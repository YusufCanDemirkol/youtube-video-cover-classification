import os
from PIL import Image

def resize_images_stretch(input_folder, output_folder, target_size=(1024, 1024)):
    """
    Görseli 1024x1024 boyutuna orijinal oranı bozmadan yeniden boyutlandırır.

    Args:
        input_folder (str): Giriş klasörünün yolu.
        output_folder (str): Çıktı klasörünün yolu.
        target_size (tuple): Yeniden boyutlandırılacak boyut (genişlik, yükseklik).

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
            output_path = os.path.join(output_folder, img_file)
            
            with Image.open(input_path) as img:
                # Görseli 1024x1024 boyutuna orijinal oranı bozmadan yeniden boyutlandır
                img_resized = img.resize(target_size, Image.Resampling.LANCZOS)
                img_resized.save(output_path)
                
                print(f"{img_file} başarıyla işlendi ve kaydedildi.")
        
        except Exception as e:
            print(f"{img_file} işlenirken hata oluştu: {e}")

    print("Tüm görseller başarıyla yeniden boyutlandırıldı.")

# Kullanım
input_folder = "C:\\Users\\HP\\Desktop\\documentary1"   # Orijinal görsellerin bulunduğu klasör
output_folder = "C:\\Users\\HP\\Desktop\\deneme" # Yeniden boyutlandırılmış görsellerin kaydedileceği klasör
resize_images_stretch(input_folder, output_folder, target_size=(1024, 1024))
