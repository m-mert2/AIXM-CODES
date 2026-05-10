import xml.etree.ElementTree as ET
import csv

def count_aixm_features_to_csv(xml_file, output_csv):
    try:
        # XML dosyasını oku
        tree = ET.parse(xml_file)
        root = tree.getroot()
    except Exception as e:
        print(f"Hata: Dosya okunamadı! {e}")
        return

    # Namespace bağımsız tüm 'hasMember' etiketlerini bul
    features = root.findall('.//{*}hasMember')
    
    total_count = len(features)
    feature_types = {}

    for member in features:
        for child in member:
            # Namespace temizleme
            tag_name = child.tag.split('}')[-1] if '}' in child.tag else child.tag
            feature_types[tag_name] = feature_types.get(tag_name, 0) + 1

    if total_count == 0:
        print("Uyarı: Hiç feature bulunamadı.")
        return

    # CSV Dosyasına Yazma İşlemi
    try:
        with open(output_csv, mode='w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            # Başlık satırı
            writer.writerow(['feature', 'count'])
            
            # Verileri satır satır yaz
            for f_type, count in sorted(feature_types.items()):
                writer.writerow([f_type, count])
        
        print(f"--- İşlem Tamamlandı ---")
        print(f"Toplam {total_count} feature bulundu.")
        print(f"Sonuçlar '{output_csv}' dosyasına kaydedildi.")
        
    except Exception as e:
        print(f"CSV yazılırken hata oluştu: {e}")

# Kullanım
count_aixm_features_to_csv('Donlon.xml', 'donlon_statistics.csv')