import os
from PIL import Image, ImageEnhance, ImageOps
import numpy as np

def augment_image(img, output_folder, base_filename):
    """
    Bir görselden veri artırımı yoluyla 6 farklı görsel oluşturur.

    Args:
        img (PIL.Image): Orijinal görsel.
        output_folder (str): Çıktı klasörünün yolu.
        base_filename (str): Orijinal dosya adı.

    Returns:
        None
    """
    # Veri artırımı için dönüşümler
    augmentations = [
        lambda x: x.transpose(Image.FLIP_LEFT_RIGHT),  # Yatay çevirme
        lambda x: x.rotate(30),                       # Saat yönünde 30 derece döndürme
        lambda x: x.rotate(-30),                      # Saat yönünün tersine 30 derece döndürme
        lambda x: ImageEnhance.Brightness(x).enhance(1.2),  # Parlaklığı biraz artırma
        lambda x: ImageEnhance.Color(x).enhance(1.5),       # Renk doygunluğunu artırma
        lambda x: add_noise(x)                             # Rastgele gürültü ekleme
    ]
    
    # Her dönüşüm için çıktı görsellerini kaydet
    for i, transform in enumerate(augmentations):
        augmented_img = transform(img)
        output_path = os.path.join(output_folder, f"{base_filename}_aug_{i+1}.jpg")
        augmented_img.save(output_path)
        print(f"{output_path} oluşturuldu.")


def add_noise(img):
    """
    Görsele rastgele gürültü ekler.

    Args:
        img (PIL.Image): Orijinal görsel.

    Returns:
        PIL.Image: Gürültü eklenmiş görsel.
    """
    np_img = np.array(img)
    noise = np.random.normal(0, 15, np_img.shape).astype(np.uint8)
    noisy_img = np.clip(np_img + noise, 0, 255).astype(np.uint8)
    return Image.fromarray(noisy_img)


def augment_images_in_folder(input_folder, output_folder):
    """
    Bir klasördeki tüm görseller için veri artırımı gerçekleştirir.

    Args:
        input_folder (str): Giriş klasörünün yolu.
        output_folder (str): Çıktı klasörünün yolu.

    Returns:
        None
    """
    # Çıkış klasörünü oluştur
    os.makedirs(output_folder, exist_ok=True)

    # Desteklenen formatlar
    supported_formats = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff')
    
    # İşlenecek görselleri al
    images = [f for f in os.listdir(input_folder) if f.lower().endswith(supported_formats)]
    
    if not images:
        print(f"Giriş klasöründe desteklenen formatlarda görsel bulunamadı: {input_folder}")
        return

    # Görselleri işlemeye başla
    for img_file in images:
        try:
            input_path = os.path.join(input_folder, img_file)
            base_filename = os.path.splitext(img_file)[0]
            
            with Image.open(input_path) as img:
                augment_image(img, output_folder, base_filename)
        
        except Exception as e:
            print(f"{img_file} işlenirken hata oluştu: {e}")

    print("Tüm görseller için veri artırımı tamamlandı.")

# Kullanım
input_folder = "C:\\Users\\HP\\Desktop\\deneme"   # Orijinal görsellerin bulunduğu klasör
output_folder = "C:\\Users\\HP\\Desktop\\belgesel arttırma 1" # Artırılmış görsellerin kaydedileceği klasör
augment_images_in_folder(input_folder, output_folder)
