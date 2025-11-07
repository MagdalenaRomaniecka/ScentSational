import time
import pandas as pd
import random
import os  
import shutil  
import tempfile 
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
# Usunęliśmy WebDriverWait, EC i By, bo ich już nie używamy

print("="*50)
print("Zaawansowany Scraper Fragrantica (Wersja 9.0 - Cierpliwy time.sleep)")
print("="*50)

# --- Konfiguracja ---
urls_to_scrape = {
    "WSZECH_CZASOW": "https://www.fragrantica.com/awards/2024/best-perfumes-of-all-time",
    "NAJLEPSZE_2024": "https://www.fragrantica.com/awards/2024/best-perfume-2024"
}

# Tworzymy losową i unikalną nazwę folderu profilu
random_id = random.randint(10000, 99999) 
temp_profile_dir = os.path.join(tempfile.gettempdir(), f"selenium_temp_profile_{random_id}")
print(f"Używam tymczasowego folderu profilu: {temp_profile_dir}")


print("Inicjalizuję sterownik przeglądarki Chrome...")
try:
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-extensions") 
    options.add_argument("--no-sandbox") 
    options.add_argument("--disable-dev-shm-usage") 
    options.add_argument("--start-maximized") 
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(f"--user-data-dir={temp_profile_dir}")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    # Globalny limit czasu zostawiamy na 60 sekund
    driver.set_page_load_timeout(60) 

except Exception as e:
    print(f"BŁĄD KRYTYCZNY: Nie udało się uruchomić przeglądarki Chrome. Powód: {e}")
    exit()

print("Sterownik uruchomiony pomyślnie.")

# Przechodzimy przez każdą listę do zeskrobania
for category_name, list_url in urls_to_scrape.items():
    
    print(f"\n[KATEGORIA: {category_name}]")
    print(f"[KROK 1] Pobieranie głównej listy z: {list_url}")

    try:
        driver.get(list_url) 
        
        # --- ZMIANA: Zamiast "wait.until" używamy "time.sleep" ---
        print("Czekam 10 sekund na pełne załadowanie dynamicznej strony...")
        time.sleep(10)
        print("Lista powinna być załadowana!")
        
    except Exception as e:
        print(f"BŁĄD: Strona nie załadowała się poprawnie (przekroczono limit 60s). Powód: {e}")
        continue 

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    
    perfume_links = []
    perfume_elements = soup.find_all('h3')

    for element in perfume_elements:
        link_tag = element.find('a')
        if link_tag and 'href' in link_tag.attrs:
            full_link = 'https://www.fragrantica.com' + link_tag['href']
            perfume_links.append(full_link)
    
    if not perfume_links:
        print("Nie znaleziono żadnych linków na stronie (mimo 10s oczekiwania). Przechodzę dalej.")
        continue

    print(f"Sukces! Znaleziono {len(perfume_links)} linków do przeanalizowania.")

    # --- Krok 2: Scraping danych z każdej podstrony ---
    print(f"[KROK 2] Rozpoczynam pobieranie danych dla {len(perfume_links)} perfum...")
    all_perfumes_data = []

    for i, link in enumerate(perfume_links, 1):
        wait_time = random.uniform(2.0, 4.0) 
        print(f"\n({i}/{len(perfume_links)}) Czekam {wait_time:.2f}s...")
        time.sleep(wait_time) 
        print(f"Przetwarzanie: {link}")

        try:
            driver.get(link) 
            
            # --- ZMIANA: Czekamy 5 sekund na załadowanie strony perfum ---
            print("Czekam 5 sekund na załadowanie strony perfum...")
            time.sleep(5)
            
            perfume_soup = BeautifulSoup(driver.page_source, 'html.parser')
            
            perfume_name = perfume_soup.find('main').find('h1').text.strip()
            notes_elements = perfume_soup.find_all('div', attrs={'data-testid': 'note'})
            notes = [note.text.strip() for note in notes_elements]
            
            print(f"  > Nazwa: {perfume_name}")
            print(f"  > Znalezione nuty: {len(notes)}")
            
            all_perfumes_data.append({
                'name': perfume_name,
                'notes': ', '.join(notes),
                'url': link
            })
                
        except Exception as e:
            print(f"  > BŁĄD: Wystąpił problem podczas przetwarzania {link}. Powód: {e}")

    # --- Krok 3: Zapisanie danych do pliku CSV ---
    print(f"\n[KROK 3] Zakończono zbieranie danych dla kategorii: {category_name}.")

    if all_perfumes_data:
        output_filename = f'perfumy_{category_name}.csv'
        try:
            df = pd.DataFrame(all_perfumes_data)
            df.to_csv(output_filename, index=False, encoding='utf-8')
            print(f"SUKCES! Dane zapisano do pliku: '{output_filename}'")
        except Exception as e:
            print(f"BŁĄD: Nie udało się zapisać pliku CSV. Powód: {e}")
    else:
        print("Nie zebrano żadnych danych do zapisania.")

# Na sam koniec zamykamy przeglądarkę
print("\nWszystkie zadania zakończone. Zamykam przeglądarkę.")
driver.quit()

# Sprzątamy po sobie, usuwając tymczasowy folder
try:
    print(f"Sprzątam tymczasowy folder profilu: {temp_profile_dir}")
    shutil.rmtree(temp_profile_dir)
    print("Posprzątano pomyślnie.")
except Exception as e:
    print(f"Nie udało się usunąć folderu tymczasowego ({temp_profile_dir}). Możesz go usunąć ręcznie. Powód: {e}")