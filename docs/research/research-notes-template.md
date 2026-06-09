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

## 🔢 WebSocket Secure (WSS) Adli Paket Çözümleme Sıralı Akışı

Ağ trafiği (HAR) analiz edilirken işletilen en alt seviye (Low-Level) protokol çözümleme adımları aşağıda listelenmiştir:

1. `data/traffic.har` dosyası adli bilişim standartlarında (Read-Only) belleğe alınır.
2. `log.entries` dizisindeki her bir JSON objesinin veri bütünlüğü (Checksum) doğrulanır.
3. İletişim isteklerindeki `resourceType` alanı taranarak `websocket` olan tüneller izole edilir.
4. `wss://web.whatsapp.com/ws/chat` endpoint'ine ait aktif soket bağlantısı belirlenir.
5. Soket içindeki `_webSocketMessages` dizisi zaman damgasına (timestamp) göre kronolojik sıraya dizilir.
6. Her bir frame mesajının giden (send) mi gelen (receive) mi olduğu `type` parametresinden ayırt edilir.
7. Ham payload verisinin uzunluğu (Length) byte cinsinden hesaplanır.
8. Metin tabanlı (Text) mesajlar ile ikili (Binary) mesajlar Opcode değerlerine göre (`Opcode 1` vs `Opcode 2`) ayrıştırılır.
9. Paket verisi üzerinde Shannon Entropi algoritması çalıştırılarak $H(X)$ değeri üretilir.
10. Entropi skoru 7.5 ve üzeri olan paketler "Noise Protocol ile Şifrelenmiş Oturum Trafiği" olarak etiketlenir.
11. Düşük entropili paketler RegEx imza kütüphanesiyle plaintext JWT, session_id veya JID ifşasına karşı taranır.
12. Opcode 2 olan binary paketlerin ilk byte'ından Protobuf mesaj sınırları (`Payload Bounds`) hesaplanır.
13. Protobuf Varint (Variable-Length Integer) çözücü fonksiyon tetiklenir.
14. Her byte'ın MSB (Most Significant Bit) değeri kontrol edilerek Varint okuma döngüsü sonlandırılır.
15. Ayrıştırılan bitler üzerinden `Field Number` (Alan Numarası) cımbızla çekilir.
16. Bit maskeleme (`byte & 0x07`) işlemiyle Protobuf `Wire Type` (Tel Tipi) tespit edilir.
17. Tel tipi 0 çıkan alanlar için sayısal ID çözümü (Varint Decoding) tamamlanır.
18. Tel tipi 2 çıkan uzunluk sınırlı alanlar için (Length-delimited) string okuma arabelleği (`buffer`) oluşturulur.
19. Çözülen string blokları içerisinden WhatsApp kullanıcı kimliği olan JID (`@s.whatsapp.net`) desenleri ayıklanır.
20. Noise Protocol durum makinesinde (FSM) el sıkışma fazının `Noise_XX` deseniyle uyumu denetlenir.
21. Gönderilen her paket sonrası `nonce` (mesaj sayacı) değeri yerelde 1 artırılarak senkronizasyon kontrol edilir.
22. Havuzda biriken tüm anomali logları, adli analiz çıktısı üretmek üzere `reports/analysis-report.md` dosyasına basılır.