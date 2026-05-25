# AIXM PDA Validator
## Biçimsel Diller ve Otomata — Grup 6 Final Projesi

---

## Proje Hakkında
AIXM (Aeronautical Information Exchange Model) formatındaki havacılık verilerini
Pushdown Automaton (PDA) ile sözdizimsel olarak doğrulayan web uygulaması.

---

## Kurulum

### Gereksinimler
- Python 3.8+
- Flask
- flask-cors

### Kurulum Adımları
```bash
pip install flask flask-cors
python app.py
```
Tarayıcıda aç: http://localhost:5000

---

## Dosya Yapısı

```
aixm_validator/
├── app.py              ← Flask web sunucusu (YAZILACAK)
├── pda_validator.py    ← 48 AIXM feature için PDA kuralları ✅
├── scenarios.py        ← 32 gerçek dünya senaryosu ✅
├── xml_parser.py       ← XML → token dönüştürücü (YAZILACAK)
├── templates/
│   └── index.html      ← Arayüz HTML (YAZILACAK)
└── static/
    └── app.js          ← Tüm JavaScript (YAZILACAK)
```

---

## Yapılacaklar (Uygulama Planı)

### 1. xml_parser.py
- XML string'ini alır
- `re` ile etiketleri sırayla çıkarır
- Feature ismini tespit eder (`aixm:Airspace` → `Airspace`)
- PDA'nın anlayacağı token listesi üretir
- Kapanış etiketlerini filtreler (sadece ana feature kapanışı kalır)

```
Giriş:
<aixm:Airspace>
  <gml:identifier>abc</gml:identifier>
  <aixm:timeSlice>...</aixm:timeSlice>
</aixm:Airspace>

Çıkış:
["aixm:Airspace", "gml:identifier", "aixm:timeSlice", "/aixm:Airspace"]
```

### 2. app.py
Flask sunucusu. 4 endpoint:

| Endpoint | Metod | Açıklama |
|---|---|---|
| `/` | GET | Ana sayfa |
| `/api/scenario/<id>` | GET | Senaryo verisi |
| `/api/validate_scenario/<id>` | GET | Senaryoyu çalıştır |
| `/api/validate_xml` | POST | XML doğrula |

### 3. templates/index.html
- Saf HTML, hiç JavaScript yok (Jinja2 çakışması önlemek için)
- İki sekme: Senaryolar / XML Doğrula
- Sol sidebar: 8 tema, 32 senaryo listesi
- Sağ panel: sonuçlar

### 4. static/app.js
Tüm JavaScript buraya:
- `loadScenario(id)` — senaryo yükle
- `runScenario()` — senaryoyu API'ye gönder, sonucu göster
- `validateXML()` — XML'i API'ye gönder, sonucu göster
- `animatePDA(steps)` — adım adım durum geçişi animasyonu
- `buildStepsTable(steps)` — geçiş tablosu oluştur

---

## Sistem Akışı

```
[Kullanıcı XML girer]
        ↓
[xml_parser.py] → token listesi
        ↓
[pda_validator.py] → PDA simülasyonu
        ↓
{ accepted: true/false, steps: [...], stack_history: [...] }
        ↓
[app.js] → sonucu arayüzde göster
```

---

## PDA Mantığı

Her feature için:
1. Açılış etiketi gelince → yığına PUSH
2. Alt etiketler sırayla kontrol edilir
3. Kapanış etiketi gelince → yığından POP
4. Yığın boş + q_accept → KABUL ✅
5. Beklenmeyen etiket → q_reject → RET ❌

---

## Özellikler
- 48 AIXM feature türü desteklenir
- 32 senaryo, 8 tema (Drone, İnşaat, Havalimanı, Seyrüsefer, ATC, Rota, Acil, Organizasyon)
- Kasıtlı hatalı senaryolar: 5, 8, 14 → RET davranışı gösterir
- Adım adım durum geçiş tablosu
- Yığın (stack) görselleştirmesi
