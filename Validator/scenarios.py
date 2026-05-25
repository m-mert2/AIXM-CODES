SCENARIOS = [
    # TEMA 1: Drone/UAV İhlali
    {
        "id": 1,
        "tema": "🛩️ Drone/UAV İhlali",
        "baslik": "Drone Yasak Hava Sahasına Giriyor",
        "aciklama": "Bir insansız hava aracı (drone), kısıtlı hava sahasına giriş yapmaya çalışıyor. UTM sistemi Airspace ve AirspaceLayer verilerini doğrulayarak geçişe izin verip vermeyeceğine karar veriyor.",
        "features": [
            {
                "feature": "Airspace",
                "tokens": ["aixm:Airspace", "gml:identifier", "gml:boundedBy", "aixm:timeSlice", "/aixm:Airspace"],
                "aciklama": "Kısıtlı hava sahası tanımı doğrulanıyor"
            },
            {
                "feature": "AirspaceLayer",
                "tokens": ["aixm:AirspaceLayer", "aixm:lowerLimit", "aixm:lowerLimitReference", "aixm:altitudeInterpretation", "/aixm:AirspaceLayer"],
                "aciklama": "Yükseklik katmanı sınırları kontrol ediliyor"
            }
        ],
        "sonuc_mesaji": "❌ Drone yasak bölgeye giremez! Sistem veriyi doğruladı, uçuş engellendi."
    },
    {
        "id": 2,
        "tema": "🛩️ Drone/UAV İhlali",
        "baslik": "Drone Havalimanı Yakınında Uçuyor",
        "aciklama": "Bir drone, kontrol kulesi bildirimi olmadan havalimanı yakınına yaklaşıyor. Sistem AirportHeliport ve Airspace verilerini doğrulayarak güvenli mesafeyi hesaplıyor.",
        "features": [
            {
                "feature": "AirportHeliport",
                "tokens": ["aixm:AirportHeliport", "gml:identifier", "aixm:timeSlice", "/aixm:AirportHeliport"],
                "aciklama": "Havalimanı sınırları doğrulanıyor"
            },
            {
                "feature": "Airspace",
                "tokens": ["aixm:Airspace", "gml:identifier", "aixm:timeSlice", "/aixm:Airspace"],
                "aciklama": "ATZ hava sahası kontrol ediliyor"
            }
        ],
        "sonuc_mesaji": "⚠️ Drone havalimanı yakınında! Kontrol kulesi uyarıldı, drone geri çağrılıyor."
    },
    {
        "id": 3,
        "tema": "🛩️ Drone/UAV İhlali",
        "baslik": "Drone Engel Tespiti Yapıyor",
        "aciklama": "Otonom drone, rota üzerindeki dikey engelleri tespit etmek için VerticalStructure ve ObstacleArea verilerini sorgular. Hatalı formatlı bir engel verisi sisteme gönderildi.",
        "features": [
            {
                "feature": "VerticalStructure",
                "tokens": ["aixm:VerticalStructure", "gml:identifier", "aixm:timeSlice", "aixm:name", "aixm:type", "aixm:lighted", "aixm:part", "/aixm:VerticalStructure"],
                "aciklama": "Dikey engel verisi doğrulanıyor"
            },
            {
                "feature": "ObstacleArea",
                "tokens": ["aixm:ObstacleArea", "gml:identifier", "aixm:timeSlice", "aixm:type", "aixm:reference_ownerRunway", "aixm:obstacle", "/aixm:ObstacleArea"],
                "aciklama": "Engel alanı sınırları kontrol ediliyor"
            }
        ],
        "sonuc_mesaji": "✅ Engel verisi geçerli. Drone alternatif rota hesapladı."
    },

    # TEMA 2: İnşaat ve Engel Yönetimi
    {
        "id": 4,
        "tema": "🏗️ İnşaat ve Engel Yönetimi",
        "baslik": "Yeni Bina İnşaatı Bildirimi",
        "aciklama": "Havalimanı yakınına yeni bir bina inşa ediliyor. İnşaat firması yapının koordinatlarını ve yüksekliğini AIXM formatında sisteme bildiriyor.",
        "features": [
            {
                "feature": "VerticalStructure",
                "tokens": ["aixm:VerticalStructure", "gml:identifier", "aixm:timeSlice", "aixm:name", "aixm:type", "aixm:lighted", "aixm:length", "aixm:width", "aixm:radius", "aixm:part", "/aixm:VerticalStructure"],
                "aciklama": "Yeni bina verisi sisteme kaydediliyor"
            }
        ],
        "sonuc_mesaji": "✅ Bina kaydı kabul edildi. Pilotlara NOTAM yayınlandı."
    },
    {
        "id": 5,
        "tema": "🏗️ İnşaat ve Engel Yönetimi",
        "baslik": "Vinç Kurulumu — Engel Alanı Güncellemesi",
        "aciklama": "İnşaat sahası yakınına geçici vinç kuruldu. Hem VerticalStructure hem ObstacleArea verileri güncellenmesi gerekiyor. Ancak ObstacleArea verisi hatalı gönderildi.",
        "features": [
            {
                "feature": "VerticalStructure",
                "tokens": ["aixm:VerticalStructure", "gml:identifier", "aixm:timeSlice", "aixm:name", "aixm:type", "aixm:lighted", "aixm:radius", "aixm:part", "/aixm:VerticalStructure"],
                "aciklama": "Vinç engel kaydı oluşturuluyor"
            },
            {
                "feature": "ObstacleArea",
                "tokens": ["aixm:ObstacleArea", "gml:identifier", "aixm:HATALI_ETIKET", "aixm:type", "/aixm:ObstacleArea"],
                "aciklama": "Engel alanı güncellenmesi — HATALI VERİ"
            }
        ],
        "sonuc_mesaji": "❌ ObstacleArea verisi reddedildi! Hatalı etiket tespit edildi. Vinç kaydı eksik kaldı."
    },
    {
        "id": 6,
        "tema": "🏗️ İnşaat ve Engel Yönetimi",
        "baslik": "Rüzgar Türbini Çiftliği Bildirimi",
        "aciklama": "Havalimanı çevresine rüzgar türbini çiftliği inşa ediliyor. Hem engel verisi hem de etkilenen hava sahası güncelleniyor.",
        "features": [
            {
                "feature": "VerticalStructure",
                "tokens": ["aixm:VerticalStructure", "gml:identifier", "aixm:timeSlice", "aixm:name", "aixm:type", "aixm:lighted", "aixm:group", "aixm:length", "aixm:width", "aixm:part", "aixm:annotation", "/aixm:VerticalStructure"],
                "aciklama": "Rüzgar türbini grubu kaydediliyor"
            },
            {
                "feature": "Airspace",
                "tokens": ["aixm:Airspace", "gml:identifier", "aixm:timeSlice", "/aixm:Airspace"],
                "aciklama": "Etkilenen hava sahası güncelleniyor"
            }
        ],
        "sonuc_mesaji": "✅ Türbin grubu ve hava sahası kısıtlaması sisteme eklendi."
    },

    # TEMA 3: Havalimanı Operasyonları
    {
        "id": 7,
        "tema": "🛬 Havalimanı Operasyonları",
        "baslik": "Pist Kapanışı Bildirimi",
        "aciklama": "09L/27R pisti bakım nedeniyle geçici olarak kapatılıyor. Runway ve RunwayDirection verileri güncelleniyor.",
        "features": [
            {
                "feature": "Runway",
                "tokens": ["aixm:Runway", "gml:identifier", "aixm:timeSlice", "aixm:designator", "aixm:type", "aixm:nominalLength", "aixm:nominalWidth", "aixm:surfaceProperties", "aixm:associatedAirportHeliport", "/aixm:Runway"],
                "aciklama": "Pist kapatma bildirimi doğrulanıyor"
            },
            {
                "feature": "RunwayDirection",
                "tokens": ["aixm:RunwayDirection", "gml:identifier", "aixm:timeSlice", "aixm:designator", "aixm:trueBearing", "aixm:trueBearingAccuracy", "aixm:usedRunway", "/aixm:RunwayDirection"],
                "aciklama": "Pist yön verisi güncelleniyor"
            }
        ],
        "sonuc_mesaji": "✅ Pist kapanış bildirimi kabul edildi. ATIS güncellendi, tüm sistemler bilgilendirildi."
    },
    {
        "id": 8,
        "tema": "🛬 Havalimanı Operasyonları",
        "baslik": "Yeni Pist Yönü Eklenmesi",
        "aciklama": "Havalimanına yeni bir pist yönü ekleniyor. RunwayDirection verisi sisteme gönderildi ancak zorunlu bir etiket eksik.",
        "features": [
            {
                "feature": "RunwayDirection",
                "tokens": ["aixm:RunwayDirection", "gml:identifier", "aixm:timeSlice", "aixm:trueBearing", "aixm:usedRunway", "/aixm:RunwayDirection"],
                "aciklama": "Yeni pist yönü kaydediliyor — designator eksik!"
            }
        ],
        "sonuc_mesaji": "❌ RunwayDirection verisi reddedildi! aixm:designator etiketi eksik."
    },
    {
        "id": 9,
        "tema": "🛬 Havalimanı Operasyonları",
        "baslik": "Apron Güncellenmesi",
        "aciklama": "Havalimanının kuzey apron bölgesi genişletiliyor. Apron ve AircraftStand verileri sisteme ekleniyor.",
        "features": [
            {
                "feature": "Apron",
                "tokens": ["aixm:Apron", "gml:identifier", "aixm:timeSlice", "aixm:name", "aixm:associatedAirportHeliport", "/aixm:Apron"],
                "aciklama": "Yeni apron alanı kaydediliyor"
            },
            {
                "feature": "AircraftStand",
                "tokens": ["aixm:AircraftStand", "gml:identifier", "aixm:timeSlice", "aixm:designator", "aixm:type", "aixm:location", "aixm:availability", "/aixm:AircraftStand"],
                "aciklama": "Uçak park yerleri tanımlanıyor"
            }
        ],
        "sonuc_mesaji": "✅ Apron ve park yerleri sisteme eklendi. Yer hizmetleri bilgilendirildi."
    },
    {
        "id": 10,
        "tema": "🛬 Havalimanı Operasyonları",
        "baslik": "Taksi Yolu Değişikliği",
        "aciklama": "B taksi yolu yeniden düzenleniyor. Taxiway ve TaxiwayElement verileri güncelleniyor.",
        "features": [
            {
                "feature": "Taxiway",
                "tokens": ["aixm:Taxiway", "gml:identifier", "aixm:timeSlice", "aixm:designator", "aixm:type", "aixm:associatedAirportHeliport", "/aixm:Taxiway"],
                "aciklama": "Taksi yolu tanımı güncelleniyor"
            },
            {
                "feature": "TaxiwayElement",
                "tokens": ["aixm:TaxiwayElement", "gml:identifier", "aixm:timeSlice", "aixm:type", "aixm:extent", "aixm:associatedTaxiway", "/aixm:TaxiwayElement"],
                "aciklama": "Taksi yolu segmentleri doğrulanıyor"
            }
        ],
        "sonuc_mesaji": "✅ Taksi yolu güncellemesi kabul edildi. Pilot briefing güncellendi."
    },
    {
        "id": 11,
        "tema": "🛬 Havalimanı Operasyonları",
        "baslik": "Holding Pozisyonu Güncellemesi",
        "aciklama": "Pist başındaki holding pozisyonu yeniden konumlandırıldı. TaxiHoldingPosition verisi sisteme gönderiliyor.",
        "features": [
            {
                "feature": "TaxiHoldingPosition",
                "tokens": ["aixm:TaxiHoldingPosition", "gml:identifier", "aixm:timeSlice", "aixm:designator", "aixm:type", "aixm:location", "/aixm:TaxiHoldingPosition"],
                "aciklama": "Holding pozisyonu verisi doğrulanıyor"
            },
            {
                "feature": "TaxiHoldingPositionMarking",
                "tokens": ["aixm:TaxiHoldingPositionMarking", "gml:identifier", "aixm:timeSlice", "aixm:type", "aixm:condition", "aixm:servedTaxiHoldingPosition", "/aixm:TaxiHoldingPositionMarking"],
                "aciklama": "Zemin işaretlemesi güncelleniyor"
            }
        ],
        "sonuc_mesaji": "✅ Holding pozisyonu güncellemesi kabul edildi."
    },

    # TEMA 4: Seyrüsefer ve İletişim
    {
        "id": 12,
        "tema": "📡 Seyrüsefer ve İletişim",
        "baslik": "VOR Arızası Bildirimi",
        "aciklama": "DON VOR seyrüsefer cihazı arıza verdi. Navaid ve VOR verileri güncellenerek sistem dışı alınıyor.",
        "features": [
            {
                "feature": "Navaid",
                "tokens": ["aixm:Navaid", "gml:identifier", "aixm:timeSlice", "aixm:type", "aixm:designator", "aixm:name", "aixm:navaidEquipment", "aixm:location", "/aixm:Navaid"],
                "aciklama": "VOR navaid kaydı güncelleniyor"
            },
            {
                "feature": "VOR",
                "tokens": ["aixm:VOR", "gml:identifier", "aixm:timeSlice", "aixm:frequency", "aixm:magneticVariation", "aixm:location", "/aixm:VOR"],
                "aciklama": "VOR frekans ve konum verisi doğrulanıyor"
            }
        ],
        "sonuc_mesaji": "✅ VOR arıza bildirimi kabul edildi. NOTAM yayınlandı, pilotlar bilgilendirildi."
    },
    {
        "id": 13,
        "tema": "📡 Seyrüsefer ve İletişim",
        "baslik": "ILS Kalibrasyon Güncellemesi",
        "aciklama": "09L pistinin ILS sistemi yeniden kalibre edildi. Navaid, Localizer ve Glidepath verileri aynı anda güncelleniyor.",
        "features": [
            {
                "feature": "Navaid",
                "tokens": ["aixm:Navaid", "gml:identifier", "aixm:timeSlice", "aixm:type", "aixm:designator", "aixm:name", "aixm:signalPerformance", "aixm:navaidEquipment", "aixm:location", "aixm:runwayDirection", "/aixm:Navaid"],
                "aciklama": "ILS sistem kaydı güncelleniyor"
            },
            {
                "feature": "Localizer",
                "tokens": ["aixm:Localizer", "gml:identifier", "aixm:timeSlice", "aixm:frequency", "aixm:course", "aixm:location", "aixm:servedRunwayDirection", "/aixm:Localizer"],
                "aciklama": "Localizer frekans ve kurs verisi doğrulanıyor"
            },
            {
                "feature": "Glidepath",
                "tokens": ["aixm:Glidepath", "gml:identifier", "aixm:timeSlice", "aixm:angle", "aixm:rdh", "aixm:location", "aixm:servedRunwayDirection", "/aixm:Glidepath"],
                "aciklama": "Alçalma açısı verisi doğrulanıyor"
            }
        ],
        "sonuc_mesaji": "✅ ILS kalibrasyon güncellemesi tamamlandı. CAT II operasyonlar aktif."
    },
    {
        "id": 14,
        "tema": "📡 Seyrüsefer ve İletişim",
        "baslik": "NDB Frekans Değişikliği",
        "aciklama": "BOR NDB'nin frekansı değiştirildi. Navaid ve NDB verileri güncelleniyor ancak NDB verisinde hata var.",
        "features": [
            {
                "feature": "Navaid",
                "tokens": ["aixm:Navaid", "gml:identifier", "aixm:timeSlice", "aixm:type", "aixm:designator", "aixm:name", "aixm:navaidEquipment", "aixm:location", "/aixm:Navaid"],
                "aciklama": "NDB navaid kaydı güncelleniyor"
            },
            {
                "feature": "NDB",
                "tokens": ["aixm:NDB", "gml:identifier", "aixm:timeSlice", "aixm:HATALI_ETIKET", "aixm:frequency", "/aixm:NDB"],
                "aciklama": "NDB frekans verisi — HATALI FORMAT"
            }
        ],
        "sonuc_mesaji": "❌ NDB verisi reddedildi! Hatalı etiket sırası. Frekans değişikliği uygulanamadı."
    },
    {
        "id": 15,
        "tema": "📡 Seyrüsefer ve İletişim",
        "baslik": "TACAN Güncellemesi",
        "aciklama": "Askeri havalimanındaki TACAN cihazının kanal numarası değiştirildi.",
        "features": [
            {
                "feature": "TACAN",
                "tokens": ["aixm:TACAN", "gml:identifier", "aixm:timeSlice", "aixm:channel", "aixm:location", "/aixm:TACAN"],
                "aciklama": "TACAN kanal verisi doğrulanıyor"
            },
            {
                "feature": "Navaid",
                "tokens": ["aixm:Navaid", "gml:identifier", "aixm:timeSlice", "aixm:type", "aixm:designator", "aixm:name", "aixm:navaidEquipment", "aixm:location", "/aixm:Navaid"],
                "aciklama": "TACAN navaid kaydı güncelleniyor"
            }
        ],
        "sonuc_mesaji": "✅ TACAN güncellendi. Askeri uçuş prosedürleri revize edildi."
    },
    {
        "id": 16,
        "tema": "📡 Seyrüsefer ve İletişim",
        "baslik": "Radyo Frekans Alanı Değişikliği",
        "aciklama": "Havalimanı yaklaşım sektörünün radyo frekans alanı yeniden düzenlendi.",
        "features": [
            {
                "feature": "RadioFrequencyArea",
                "tokens": ["aixm:RadioFrequencyArea", "gml:identifier", "aixm:timeSlice", "aixm:type", "aixm:extent", "/aixm:RadioFrequencyArea"],
                "aciklama": "Radyo frekans alanı verisi doğrulanıyor"
            },
            {
                "feature": "RadioCommunicationChannel",
                "tokens": ["aixm:RadioCommunicationChannel", "gml:identifier", "aixm:timeSlice", "aixm:frequencyTransmission", "aixm:frequencyReception", "aixm:type", "/aixm:RadioCommunicationChannel"],
                "aciklama": "İletişim kanalı verisi doğrulanıyor"
            }
        ],
        "sonuc_mesaji": "✅ Radyo frekans alanı güncellemesi kabul edildi."
    },

    # TEMA 5: Hava Trafik Kontrolü
    {
        "id": 17,
        "tema": "✈️ Hava Trafik Kontrolü",
        "baslik": "ATC Servis Güncellemesi",
        "aciklama": "Donlon APP frekansı değiştirildi. AirTrafficControlService verisi sisteme gönderiliyor.",
        "features": [
            {
                "feature": "AirTrafficControlService",
                "tokens": ["aixm:AirTrafficControlService", "gml:identifier", "aixm:timeSlice", "aixm:serviceProvider", "aixm:call_sign", "aixm:radioCommunication", "aixm:type", "aixm:clientAirspace", "/aixm:AirTrafficControlService"],
                "aciklama": "ATC servis verisi doğrulanıyor"
            }
        ],
        "sonuc_mesaji": "✅ ATC frekans değişikliği kabul edildi. ATIS güncellendi."
    },
    {
        "id": 18,
        "tema": "✈️ Hava Trafik Kontrolü",
        "baslik": "FIR Sınırı Değişikliği",
        "aciklama": "Donlon FIR'ının batı sınırı komşu ülkeyle yapılan anlaşma doğrultusunda güncelleniyor.",
        "features": [
            {
                "feature": "Airspace",
                "tokens": ["aixm:Airspace", "gml:identifier", "gml:boundedBy", "aixm:timeSlice", "/aixm:Airspace"],
                "aciklama": "FIR hava sahası sınırı güncelleniyor"
            },
            {
                "feature": "GeoBorder",
                "tokens": ["aixm:GeoBorder", "gml:identifier", "aixm:timeSlice", "aixm:type", "aixm:extent", "/aixm:GeoBorder"],
                "aciklama": "Coğrafi sınır verisi doğrulanıyor"
            }
        ],
        "sonuc_mesaji": "✅ FIR sınır değişikliği kabul edildi. ICAO bilgilendirildi."
    },
    {
        "id": 19,
        "tema": "✈️ Hava Trafik Kontrolü",
        "baslik": "TMA Aktivasyonu",
        "aciklama": "Donlon TMA'sı yoğun trafik nedeniyle geçici olarak genişletildi. Airspace ve AirspaceLayer verileri güncelleniyor.",
        "features": [
            {
                "feature": "Airspace",
                "tokens": ["aixm:Airspace", "gml:identifier", "aixm:timeSlice", "/aixm:Airspace"],
                "aciklama": "TMA hava sahası aktivasyonu doğrulanıyor"
            },
            {
                "feature": "AirspaceLayer",
                "tokens": ["aixm:AirspaceLayer", "aixm:upperLimit", "aixm:upperLimitReference", "aixm:lowerLimit", "aixm:lowerLimitReference", "aixm:altitudeInterpretation", "/aixm:AirspaceLayer"],
                "aciklama": "TMA yükseklik katmanı doğrulanıyor"
            }
        ],
        "sonuc_mesaji": "✅ TMA genişletme aktivasyonu kabul edildi. Pilotlar NOTAM ile bilgilendirildi."
    },
    {
        "id": 20,
        "tema": "✈️ Hava Trafik Kontrolü",
        "baslik": "Askeri Hava Sahası Aktivasyonu",
        "aciklama": "MOA (Military Operating Area) tatbikat nedeniyle aktive ediliyor. Sivil uçuşlar için kısıtlama uygulanacak.",
        "features": [
            {
                "feature": "Airspace",
                "tokens": ["aixm:Airspace", "gml:identifier", "gml:boundedBy", "aixm:timeSlice", "/aixm:Airspace"],
                "aciklama": "Askeri hava sahası verisi doğrulanıyor"
            },
            {
                "feature": "AirspaceLayer",
                "tokens": ["aixm:AirspaceLayer", "aixm:discreteLevelSeries", "/aixm:AirspaceLayer"],
                "aciklama": "Kısıtlama yükseklik seviyesi doğrulanıyor"
            }
        ],
        "sonuc_mesaji": "✅ MOA aktivasyonu kabul edildi. Sivil uçuşlar alternatif rotaya yönlendirildi."
    },

    # TEMA 6: Rota ve Nokta Yönetimi
    {
        "id": 21,
        "tema": "🗺️ Rota ve Nokta Yönetimi",
        "baslik": "Yeni Rota Segmenti Eklenmesi",
        "aciklama": "Donlon - Amswell arası yeni bir hava yolu segmenti ekleniyor. Route ve RouteSegment verileri sisteme gönderiliyor.",
        "features": [
            {
                "feature": "Route",
                "tokens": ["aixm:Route", "gml:identifier", "aixm:timeSlice", "aixm:designator", "aixm:type", "aixm:flightRule", "/aixm:Route"],
                "aciklama": "Hava yolu tanımı doğrulanıyor"
            },
            {
                "feature": "RouteSegment",
                "tokens": ["aixm:RouteSegment", "gml:identifier", "aixm:timeSlice", "aixm:level", "aixm:start", "aixm:end", "aixm:routeFormed", "/aixm:RouteSegment"],
                "aciklama": "Rota segmenti verisi doğrulanıyor"
            }
        ],
        "sonuc_mesaji": "✅ Yeni rota segmenti kabul edildi. Uçuş planlaması güncellendi."
    },
    {
        "id": 22,
        "tema": "🗺️ Rota ve Nokta Yönetimi",
        "baslik": "Waypoint Güncellemesi",
        "aciklama": "KANAD waypoint'inin koordinatları GPS doğrulaması sonrası güncelleniyor.",
        "features": [
            {
                "feature": "DesignatedPoint",
                "tokens": ["aixm:DesignatedPoint", "gml:identifier", "aixm:timeSlice", "aixm:designator", "aixm:type", "aixm:location", "/aixm:DesignatedPoint"],
                "aciklama": "Waypoint koordinat verisi doğrulanıyor"
            }
        ],
        "sonuc_mesaji": "✅ Waypoint güncellemesi kabul edildi. FMS veritabanları güncellendi."
    },
    {
        "id": 23,
        "tema": "🗺️ Rota ve Nokta Yönetimi",
        "baslik": "Holding Pattern Değişikliği",
        "aciklama": "DON VOR üzerindeki bekleme prosedürü değiştirildi. HoldingPattern verisi güncelleniyor.",
        "features": [
            {
                "feature": "HoldingPattern",
                "tokens": ["aixm:HoldingPattern", "gml:identifier", "aixm:timeSlice", "aixm:inboundCourse", "aixm:turnDirection", "aixm:fix", "/aixm:HoldingPattern"],
                "aciklama": "Bekleme prosedürü verisi doğrulanıyor"
            }
        ],
        "sonuc_mesaji": "✅ Holding pattern değişikliği kabul edildi. Approach chart güncellendi."
    },
    {
        "id": 24,
        "tema": "🗺️ Rota ve Nokta Yönetimi",
        "baslik": "Geçiş Noktası Güncellemesi",
        "aciklama": "İki VOR arasındaki sinyal değişim noktası yeniden hesaplandı.",
        "features": [
            {
                "feature": "ChangeOverPoint",
                "tokens": ["aixm:ChangeOverPoint", "gml:identifier", "aixm:timeSlice", "aixm:distance", "aixm:routeSegment", "/aixm:ChangeOverPoint"],
                "aciklama": "Geçiş noktası verisi doğrulanıyor"
            },
            {
                "feature": "AngleIndication",
                "tokens": ["aixm:AngleIndication", "gml:identifier", "aixm:timeSlice", "aixm:angle", "aixm:angleType", "aixm:indicationDirection", "aixm:fix", "/aixm:AngleIndication"],
                "aciklama": "VOR radyal açı verisi doğrulanıyor"
            }
        ],
        "sonuc_mesaji": "✅ Geçiş noktası güncellemesi kabul edildi."
    },

    # TEMA 7: Acil ve Güvenlik
    {
        "id": 25,
        "tema": "🚨 Acil ve Güvenlik",
        "baslik": "Arama Kurtarma Bölgesi Aktivasyonu",
        "aciklama": "Denizde bir uçak kayboldu. SAR operasyonu başlatılıyor, arama bölgesi AIXM ile sisteme bildiriliyor.",
        "features": [
            {
                "feature": "SearchRescueService",
                "tokens": ["aixm:SearchRescueService", "gml:identifier", "aixm:timeSlice", "aixm:serviceProvider", "aixm:type", "/aixm:SearchRescueService"],
                "aciklama": "SAR servis aktivasyonu doğrulanıyor"
            },
            {
                "feature": "Airspace",
                "tokens": ["aixm:Airspace", "gml:identifier", "gml:boundedBy", "aixm:timeSlice", "/aixm:Airspace"],
                "aciklama": "SAR operasyon bölgesi hava sahası tanımlanıyor"
            }
        ],
        "sonuc_mesaji": "🚨 SAR operasyonu başlatıldı! Bölge hava sahası koordineli olarak tahsis edildi."
    },
    {
        "id": 26,
        "tema": "🚨 Acil ve Güvenlik",
        "baslik": "NOTAM — Geçici Kısıtlama",
        "aciklama": "VIP uçuş nedeniyle geçici hava sahası kısıtlaması (TFR) uygulanıyor. Airspace ve AirspaceLayer verileri ile Dijital NOTAM yayınlanıyor.",
        "features": [
            {
                "feature": "Airspace",
                "tokens": ["aixm:Airspace", "gml:identifier", "aixm:timeSlice", "/aixm:Airspace"],
                "aciklama": "TFR hava sahası tanımı doğrulanıyor"
            },
            {
                "feature": "AirspaceLayer",
                "tokens": ["aixm:AirspaceLayer", "aixm:lowerLimit", "aixm:lowerLimitReference", "aixm:altitudeInterpretation", "/aixm:AirspaceLayer"],
                "aciklama": "Kısıtlama yükseklik katmanı doğrulanıyor"
            }
        ],
        "sonuc_mesaji": "✅ TFR NOTAM yayınlandı. Etkilenen uçuşlar reroute edildi."
    },
    {
        "id": 27,
        "tema": "🚨 Acil ve Güvenlik",
        "baslik": "Pist İşaretleme Güncellemesi",
        "aciklama": "27R pistinin threshold işaretlemesi yenilendi. RunwayMarking verisi sisteme gönderiliyor.",
        "features": [
            {
                "feature": "RunwayMarking",
                "tokens": ["aixm:RunwayMarking", "gml:identifier", "aixm:timeSlice", "aixm:type", "aixm:condition", "aixm:servedRunwayDirection", "/aixm:RunwayMarking"],
                "aciklama": "Pist işaretleme verisi doğrulanıyor"
            },
            {
                "feature": "RunwayCentrelinePoint",
                "tokens": ["aixm:RunwayCentrelinePoint", "gml:identifier", "aixm:timeSlice", "aixm:role", "aixm:location", "aixm:usedRunway", "/aixm:RunwayCentrelinePoint"],
                "aciklama": "Merkez hat noktası verisi doğrulanıyor"
            }
        ],
        "sonuc_mesaji": "✅ Pist işaretleme güncellemesi kabul edildi. AIP yayınlandı."
    },
    {
        "id": 28,
        "tema": "🚨 Acil ve Güvenlik",
        "baslik": "Yaklaşma Işıklandırması Arızası",
        "aciklama": "09R pistinin CAT II yaklaşma ışık sistemi arızalandı. ApproachLightingSystem verisi güncelleniyor.",
        "features": [
            {
                "feature": "ApproachLightingSystem",
                "tokens": ["aixm:ApproachLightingSystem", "gml:identifier", "aixm:timeSlice", "aixm:type", "aixm:classICAO", "aixm:length", "aixm:element", "aixm:servedRunwayDirection", "/aixm:ApproachLightingSystem"],
                "aciklama": "Yaklaşma ışık sistemi verisi doğrulanıyor"
            },
            {
                "feature": "RunwayDirectionLightSystem",
                "tokens": ["aixm:RunwayDirectionLightSystem", "gml:identifier", "aixm:timeSlice", "aixm:type", "aixm:servedRunwayDirection", "/aixm:RunwayDirectionLightSystem"],
                "aciklama": "Pist ışıklandırma sistemi verisi doğrulanıyor"
            }
        ],
        "sonuc_mesaji": "⚠️ CAT II operasyonlar askıya alındı! NOTAM yayınlandı, CAT I minimum uygulandı."
    },

    # TEMA 8: Organizasyon ve Servis
    {
        "id": 29,
        "tema": "🏢 Organizasyon ve Servis",
        "baslik": "Yeni Otorite Kaydı",
        "aciklama": "Donlon Sivil Havacılık Otoritesi sisteme yeni bir alt birim kaydediyor.",
        "features": [
            {
                "feature": "OrganisationAuthority",
                "tokens": ["aixm:OrganisationAuthority", "gml:identifier", "aixm:timeSlice", "aixm:name", "aixm:type", "aixm:designator", "/aixm:OrganisationAuthority"],
                "aciklama": "Organizasyon kayıt verisi doğrulanıyor"
            },
            {
                "feature": "AuthorityForAirspace",
                "tokens": ["aixm:AuthorityForAirspace", "gml:identifier", "aixm:timeSlice", "aixm:type", "aixm:theAirspace", "aixm:theUnit", "/aixm:AuthorityForAirspace"],
                "aciklama": "Hava sahası otorite ataması doğrulanıyor"
            }
        ],
        "sonuc_mesaji": "✅ Yeni otorite kaydı sisteme eklendi."
    },
    {
        "id": 30,
        "tema": "🏢 Organizasyon ve Servis",
        "baslik": "Bilgi Servisi Güncellemesi",
        "aciklama": "ATIS yayın servisi yeni frekansla güncelleniyor.",
        "features": [
            {
                "feature": "InformationService",
                "tokens": ["aixm:InformationService", "gml:identifier", "aixm:timeSlice", "aixm:serviceProvider", "aixm:type", "aixm:radioCommunication", "/aixm:InformationService"],
                "aciklama": "Bilgi servisi verisi doğrulanıyor"
            },
            {
                "feature": "Unit",
                "tokens": ["aixm:Unit", "gml:identifier", "aixm:timeSlice", "aixm:name", "aixm:type", "aixm:designator", "/aixm:Unit"],
                "aciklama": "Birim kaydı doğrulanıyor"
            }
        ],
        "sonuc_mesaji": "✅ ATIS frekans güncellemesi kabul edildi."
    },
    {
        "id": 31,
        "tema": "🏢 Organizasyon ve Servis",
        "baslik": "Özel Tarih Tanımlaması",
        "aciklama": "Ulusal bayram günü için özel operasyon saatleri tanımlanıyor.",
        "features": [
            {
                "feature": "SpecialDate",
                "tokens": ["aixm:SpecialDate", "gml:identifier", "aixm:timeSlice", "aixm:dateYear", "aixm:dateMonth", "aixm:dateDay", "aixm:type", "/aixm:SpecialDate"],
                "aciklama": "Özel tarih verisi doğrulanıyor"
            },
            {
                "feature": "AirportHeliport",
                "tokens": ["aixm:AirportHeliport", "gml:identifier", "aixm:timeSlice", "/aixm:AirportHeliport"],
                "aciklama": "Havalimanı operasyon saatleri güncelleniyor"
            }
        ],
        "sonuc_mesaji": "✅ Özel tarih operasyon planı kabul edildi."
    },
    {
        "id": 32,
        "tema": "🏢 Organizasyon ve Servis",
        "baslik": "Yer Işıklandırma Sistemi Güncellemesi",
        "aciklama": "Havalimanı apron ışıklandırma sistemi yenilendi. AeronauticalGroundLight ve GuidanceLine verileri güncelleniyor.",
        "features": [
            {
                "feature": "AeronauticalGroundLight",
                "tokens": ["aixm:AeronauticalGroundLight", "gml:identifier", "aixm:timeSlice", "aixm:name", "aixm:type", "aixm:colour", "aixm:flashing", "aixm:location", "/aixm:AeronauticalGroundLight"],
                "aciklama": "Yer ışığı verisi doğrulanıyor"
            },
            {
                "feature": "GuidanceLine",
                "tokens": ["aixm:GuidanceLine", "gml:identifier", "aixm:timeSlice", "aixm:type", "aixm:extent", "aixm:associatedTaxiway", "/aixm:GuidanceLine"],
                "aciklama": "Yönlendirme çizgisi verisi doğrulanıyor"
            },
            {
                "feature": "GuidanceLineMarking",
                "tokens": ["aixm:GuidanceLineMarking", "gml:identifier", "aixm:timeSlice", "aixm:type", "aixm:condition", "aixm:servedGuidanceLine", "/aixm:GuidanceLineMarking"],
                "aciklama": "Yönlendirme işaretlemesi doğrulanıyor"
            }
        ],
        "sonuc_mesaji": "✅ Yer ışıklandırma sistemi güncellemesi kabul edildi."
    },
]
