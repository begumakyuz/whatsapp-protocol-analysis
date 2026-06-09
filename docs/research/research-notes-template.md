# 🧬 WhatsApp Web Protokolü Tersine Mühendislik Araştırma Notları

> **Ders:** BGT210 Tersine Mühendislik (Reverse Engineering)  
> **Danışman / Instructor:** Keyvan Arasteh  
> **Tarih:** 10 Haziran 2026  

---

## 🔍 Araştırılan Konu: WhatsApp Web Protokol Mimarisi
WhatsApp Web (`web.whatsapp.com`), geleneksel HTTP REST API mimarileri yerine, iki yönlü (bi-directional), düşük gecikmeli ve sürekli açık kalan **WebSocket Secure (WSS)** tünelleri üzerinden haberleşir. Bu tünel üzerinde uçtan uca şifrelemeyi (E2EE) tarayıcı katmanında korumak amacıyla **Noise Protocol Framework** şemalarını kullanır.

## 🛠️ Protokolün Çözülme Metodolojisi (Baileys & Evolution API Yaklaşımı)
Açık kaynak dünyasındaki tersine mühendislik projeleri, WhatsApp'ın web istemcisinin JavaScript kaynak kodlarını (özellikle obfuscate edilmiş ana tünel scriptlerini) deobfuscate ederek şu üç temel mekanizmayı çözmüştür:

1. **Noise Handshake (El Sıkışma):** İstemci ve sunucu haberleşmeye başlarken `Noise_XX_25519_AESGCM_SHA256` protokol deseni üzerinden el sıkışır. Curve25519 Ephemeral Key üretimi tarayıcıda statik olarak tetiklenir.
2. **Protobuf Serileştirme (Protocol Buffers):** WhatsApp, ağ paketlerinin boyutunu minimize etmek için verileri JSON olarak değil, ikili (binary) Protobuf formatında taşır. Her bir paket belirli alan numaralarına (Field Numbers) ve tel tiplerine (Wire Types) sahiptir.
3. **Oturum Kalıcılığı (Session Persistence):** Kimlik doğrulama tamamlandıktan sonra türetilen şifreleme anahtarları tarayıcının `IndexedDB` veya `LocalStorage` katmanında saklanır.

## 🛑 Derste İşlenen Ağ İzleme Adımlarının Tekrarı
1. **Veri Yakalama (Capture):** Tarayıcı DevTools (F12) Network paneli açılarak `WS` filtresi filtrelenmiş ve `wss://web.whatsapp.com/ws/chat` tüneli canlı takibe alınmıştır.
2. **Analiz (Read):** Akan metin (Text) tabanlı frame'ler içinden el sıkışma parametreleri saptanmış, ikili (Binary) frame'ler ise hex formatında dışa aktarılmıştır.
3. **HAR Export:** Tüm bu akış, adli bilişim kanıtı ve parser girdisi olarak `traffic.har` formatında diske kaydedilmiştir.