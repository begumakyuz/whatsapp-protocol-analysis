# DeepSearch Analiz Çıktısı

Merhaba! Bir Kıdemli Tersine Mühendis ve Siber Güvenlik Uzmanı olarak, İstinye Üniversitesi BGT210 standartlarına ve endüstriyel Defansif Programlama pratiklerine uygun bir "WhatsApp Protocol Forensic Framework" inşa etmen için ihtiyacın olan derinlemesine yol haritasını aşağıda sunuyorum.

## 1. Hazırlık ve Veri Toplama Aşaması (HAR & WebSocket Analizi)

Projeye sıfırdan başlarken elinde gerçek bir veri seti (ground truth) olması şarttır. WhatsApp Web'in trafiğini dinlemek için bir Man-in-the-Middle (MitM) proxy kullanmak yerine pasif bir yaklaşım sergilemek daha kolay ve yasaldır:

- **Browser DevTools Kullanımı:** Tarayıcından WhatsApp Web'e girip F12 ile Network sekmesini aç. Filtrelerden `WS` (WebSocket) seç. `wss://web.whatsapp.com/ws/chat` endpoint'ine giden paketleri izle.
- **HAR Export:** Oturum açılışından itibaren el sıkışmayı yakalamak için Network loglarını `.har` (HTTP Archive) formatında dışa aktar. Bu JSON tabanlı bir formattır ve WebSocket frame'lerinin `opcode`, `data` ve `type` bilgilerini barındırır.
- **Ayrıştırma (Parsing):** Python'da `json` kütüphanesi ile HAR dosyasını oku. İlgili `_webSocketMessages` dizilerini filtreleyerek Opcode 1 (Text) ve Opcode 2 (Binary) ayrımını yap.

## 2. Kriptografik Entropi Analizi

WebSocket tünelinden akan verilerin açık metin mi (Plaintext) yoksa şifreli mi (Ciphertext) olduğunu anlamak için Shannon Entropisi kullanılmalıdır.
- **Tip Güvenliği (Kritik):** Entropi hesaplarken verinin `bytes` olduğundan emin olmalısın. Eğer HAR içindeki veriler base64 veya raw string olarak geliyorsa, bunları `encode('utf-8', errors='ignore')` ile zorla dönüştürmek, binary paketlerin veri bütünlüğünü bozacaktır. Katı `isinstance(payload, bytes)` kontrolleri kullan.
- **Entropi Sınırları:** AES-GCM ve Curve25519 paketleri yüksek bir rastgeleliğe sahiptir. Hesaplanan Shannon Entropisi 7.5 ve üzerindeyse verinin Noise protokolü ile sıkı bir şekilde şifrelendiğini kabul edebilirsin.

## 3. Protobuf (Protocol Buffers) Tersine Mühendisliği

WhatsApp binary verilerini Protobuf formatında gönderir. Bu verileri de-serialize ederken:
- **Wire Type & Field Number:** Protobuf spesifikasyonlarını iyi öğrenmeli ve Tag ayrıştırmasını (Tag = Field Number << 3 | Wire Type) kurgulamalısın.
- **Varint DoS Koruması (Defansif Pratik):** Protobuf içerisinde değişken uzunluklu integer'lar (Varint) sıklıkla kullanılır. Varint okuyan `while` döngüne bir güvenlik sınırı ekle (örneğin `shift >= 64` olduğunda exception fırlat). Yoksa kötü niyetli veya bozuk bir frame, analiz motorunu sonsuz döngüye sokup OOM (Out Of Memory) veya CPU DoS zafiyetine yol açabilir.

## 4. Noise Protocol El Sıkışması ve FSM (Finite State Machine)

WhatsApp'ın kullandığı `Noise_XX_25519_AESGCM_SHA256` şemasını analiz etmek için bir durum makinesi (FSM) yaz:
- **Aşamalar:** `EPHEMERAL_EXCHANGE`, `SERVER_RESPONSE_WAIT`, `CLIENT_FINAL_SIGN`, `COMPLETED`.
- **Simülasyon Mantığı:** Amacın şifreyi kırmak değil, protokolü simüle etmek olduğu için `mix_key` ve `mix_hash` aşamalarında sahte (dummy) Diffie-Hellman anahtarları (örneğin `b"\xaa" * 32`) kullanarak HKDF zincirinin matematiksel adımlarını kodlayabilirsin.

## 5. Mimari Kurulum, TDD ve Mypy Uyumlu Kalite Standartları

BGT210 ve endüstri standartlarına uygun bir proje yapısı şu şekilde olmalıdır:

- **Modülerlik:** `src/core/` altında `parser.py`, `protobuf.py`, `crypto_handshake.py` modülleri olsun. `main.py` ise sadece CLI orkestrasyonunu (Argparse) yönetsin.
- **Type Hinting & Mypy:** Python kodlarında katı statik tip denetimleri (`Dict`, `List`, `Union`, `TypedDict`) kullan. Parametrelerin içine ne gireceğini açıkça belirt.
- **Test Driven Development (TDD):** Kod yazmadan önce (veya eşzamanlı olarak) `tests/` klasörü altında `pytest` ile testlerini yaz. Testlerin daima asıl sınıfların güncel metod adlarıyla (`CryptographicAnalyzer.calculate_shannon_entropy` vb.) %100 senkronize olmasını sağla. Aksi takdirde CI/CD pipeline'ın çalışmaz.
- **Otomatik Raporlama:** Analiz sonuçlarını doğrudan konsola basmak yerine, Markdown tabanlı bir `reports/analysis-report.md` dosyası oluşturarak siber tehdit avcılığı (DPI) bulgularını (Olası token sızıntıları, entropi seviyeleri) akademik bir rapor formatında diske yazdır.

Bu adımları izleyerek sıfırdan kuracağın framework, hem mükemmel bir siber güvenlik projesi hem de endüstriyel kalitede bir adli analiz aracı (SecOps Auditor) olacaktır. Başarılar dilerim!
