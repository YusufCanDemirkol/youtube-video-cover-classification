import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

# YouTube arama sonuçları URL'si
url = "https://www.youtube.com/results?search_query=online+write++education"

# Tarayıcı ayarları
options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:118.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36")
options.add_argument('--headless')
options.add_argument('--incognito')





driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get(url)


scroll_pause_time = 5  
max_scrolls = 200  
min_required_images = 400  

last_height = driver.execute_script("return document.documentElement.scrollHeight")
image_urls = set()

for i in range(max_scrolls):
    print(f"Kaydırma {i+1} yapılıyor...")
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    time.sleep(scroll_pause_time)

   
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    for img_tag in soup.find_all('img'):
        img_url = img_tag.get('src')
        img_class = img_tag.get('class', [])

        
        if not img_url:
            continue

        # Shorts videolarını filtrele (Shorts içeren class'ları veya dikey formatları atla)
        if "ShortsLockupViewModelHostThumbnail" in img_class or "oardefault" in img_url:
            continue

        
        if img_url and "i.ytimg.com" in img_url:
            image_urls.add(img_url)

    print(f"Şu ana kadar bulunan kapak fotoğrafı: {len(image_urls)}")

    
    if len(image_urls) >= min_required_images:
        print(f"İstenen görsel miktarına ulaşıldı ({min_required_images}). Kaydırma durduruluyor.")
        break

   
    new_height = driver.execute_script("return document.documentElement.scrollHeight")
    if new_height == last_height:
        print("Daha fazla içerik yüklenemiyor, kaydırma durduruldu.")
        break
    last_height = new_height

driver.quit()


print(f"Toplam bulunan kapak fotoğrafı: {len(image_urls)}")


if not os.path.exists('youtube_thumbnails'):
    os.makedirs('youtube_thumbnails')


existing_files = set(os.listdir('youtube_thumbnails'))
existing_files_ids = {int(f.split('_')[1].split('.')[0]) for f in existing_files if f.startswith('thumbnail')}


# İndirme işlemi mevcut dosya sayısından başlar
indirilen_sayi = max(existing_files_ids, default=0)
maks_indirilecek = 400  
for img_url in image_urls:
    try:
        indirilen_sayi += 1
        dosya_adi = f"thumbnail_{indirilen_sayi}.jpg"
        dosya_yolu = os.path.join('youtube_thumbnails', dosya_adi)

        # Fotoğrafı indir ve kaydet
        img_data = requests.get(img_url, timeout=10).content
        with open(dosya_yolu, 'wb') as img_file:
            img_file.write(img_data)

        print(f"{indirilen_sayi}. kapak fotoğrafı indirildi: {img_url}")

        # Maksimum indirme sınırına ulaşıldığında dur
        if indirilen_sayi - max(existing_files_ids, default=0) >= maks_indirilecek:
            break
    except Exception as e:
        print(f"Kapak fotoğrafı indirilemedi: {e}")






