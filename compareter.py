import csv

def compare_csvs(file1, file2):
    def load_to_dict(filename):
        data = {}
        try:
            with open(filename, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # feature ismini anahtar, sayıyı değer yapıyoruz
                    data[row['feature']] = int(row['count'])
        except Exception as e:
            print(f"Hata: {filename} okunamadı. {e}")
        return data

    dict1 = load_to_dict(file1)
    dict2 = load_to_dict(file2)

    if not dict1 or not dict2:
        return

    # Tüm benzersiz feature isimlerini topla (her iki dosyada olanlar)
    all_features = set(dict1.keys()).union(set(dict2.keys()))
    
    matches = 0
    total = len(all_features)

    print(f"\n--- Karşılaştırma Raporu ---")
    print(f"{'Feature':<30} | {'CSV 1':<8} | {'CSV 2':<8} | Durum")
    print("-" * 65)

    for feat in sorted(all_features):
        val1 = dict1.get(feat, 0)
        val2 = dict2.get(feat, 0)
        
        status = "✅ OK" if val1 == val2 else "❌ FARK"
        if val1 == val2:
            matches += 1
            
        print(f"{feat:<30} | {val1:<8} | {val2:<8} | {status}")

    # Benzerlik hesaplama
    similarity = (matches / total) * 100 if total > 0 else 0

    print("-" * 65)
    print(f"Toplam Farklı Tip Sayısı : {total}")
    print(f"Tam Eşleşen Tip Sayısı   : {matches}")
    print(f"Benzerlik Oranı          : %{similarity:.2f}")

# Kullanım
compare_csvs('aixm_results.csv', 'donlon_statistics.csv')