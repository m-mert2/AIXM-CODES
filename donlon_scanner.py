"""
AIXM Feature Tipi Tarayıcı v2 (CSV Destekli)
Kullanım: python aixm_scanner.py Donlon.xml
"""

import xml.etree.ElementTree as ET
from collections import defaultdict
import sys, os, re
import csv

def scan_aixm(filepath):
    print(f"\nDosya taranıyor: {filepath}")
    print(f"Boyut: {os.path.getsize(filepath) / 1024 / 1024:.1f} MB\n")

    feature_counts   = defaultdict(int)
    feature_children = defaultdict(set)

    AIXM_NS = "http://www.aixm.aero/schema/5.1.1"

    in_feature   = None
    in_timeslice = False
    depth_stack  = []

    # PARSE MANTIĞI (DOKUNULMADI) 
    for event, elem in ET.iterparse(filepath, events=("start", "end")):
        m = re.match(r'\{([^}]+)\}(.+)', elem.tag)
        if not m:
            continue
        ns, local = m.group(1), m.group(2)

        if event == "start":
            depth_stack.append((ns, local))

            if ns == AIXM_NS and local[0].isupper() and not local.endswith("TimeSlice"):
                if len(depth_stack) >= 2:
                    _, parent_local = depth_stack[-2]
                    if parent_local == "hasMember":
                        in_feature = local
                        feature_counts[local] += 1
                        in_timeslice = False

            if in_feature and local.endswith("TimeSlice") and ns == AIXM_NS:
                in_timeslice = True

            if in_timeslice and ns == AIXM_NS and not local.endswith("TimeSlice") \
               and not local[0].isupper():
                feature_children[in_feature].add(local)

        elif event == "end":
            if depth_stack:
                depth_stack.pop()
            if in_feature and ns == AIXM_NS and local == in_feature:
                in_feature   = None
                in_timeslice = False
            elem.clear()

    # --- ÇIKTI TÜRÜ DEĞİŞİMİ (CSV YAZMA) ---
    output_filename = "aixm_results.csv"
    try:
        with open(output_filename, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['feature', 'count'])  # Başlıklar
            # Sayıya göre çoktan aza sıralı yaz
            for ft, count in sorted(feature_counts.items(), key=lambda x: -x[1]):
                writer.writerow([ft, count])
        print(f"✔ Başarıyla kaydedildi: {output_filename}")
    except Exception as e:
        print(f"❌ CSV yazma hatası: {e}")

    # Terminal Özeti (Görsel takip için)
    print("=" * 62)
    print(f" Toplam feature örneği : {sum(feature_counts.values())}")
    print("=" * 62)
    
    # Alt etiketleri terminalde göstermeye devam et (CSV'ye dahil edilmez)
    print(f"\n  ALT ETİKETLER (Terminal Bilgilendirme):\n")
    for ft in sorted(feature_counts.keys()):
        children = sorted(feature_children.get(ft, []))
        if children:
            print(f"  {ft} ({len(children)} alan)")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Kullanim: python aixm_scanner.py <dosya.xml>")
        sys.exit(1)
    scan_aixm(sys.argv[1])