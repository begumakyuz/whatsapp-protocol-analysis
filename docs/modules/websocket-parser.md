# 📑 Modül Dokümantasyonu: Gelişmiş WebSocket, Noise Handshake ve Protobuf Ayrıştırıcı (DPI Engine)

> **Akademik Kurum:** İstinye Üniversitesi (İSU)  
> **Ders Kodu ve Adı:** BGT210 - Tersine Mühendislik (Reverse Engineering)  
> **Danışman / Instructor:** Keyvan Arasteh  
> **Geliştirici:** Begüm Akyüz - 2420**1005  

---

## 🗺️ İçindekiler
1. [Modülün Amacı ve Kapsamı](#1-modülün-amacı-ve-kapsamı)
2. [Protokol ve Mimari Akış Şeması](#2-protokol-ve-mimari-akış-şeması)
3. [Algoritma ve Durum Makinesi (FSM) Mantığı](#3-algoritma-ve-durum-makinesi-fsm-mantığı)
4. [Kriptografik ve Ofansif Analiz Parametreleri](#4-kriptografik-ve-ofansif-analiz-parametreleri)
5. [Kurulum, Entegrasyon ve Test Senaryoları](#5-kurulum-entegrasyon-ve-test-senaryoları)
6. [Bilinen Kısıtlamalar ve Gelecek Geliştirmeler](#6-bilinen-kısıtlamalar-ve-gelecek-geliştirmeler)

---

## 1. Modülün Amacı ve Kapsamı
Bu modül (`src/core/parser.py`), `web.whatsapp.com` (WhatsApp Web) platformunun tarayıcı tabanlı kapalı devre iletişim protokolünü de-serialize etmek ve siber güvenlik mukavemetini ölçmek amacıyla tasarlanmış ana analiz çekirdeğidir. 

Geleneksel imza tabanlı HTTP proxy araçlarının yetersiz kaldığı durumlarda, iki yönlü (bi-directional) WebSocket Secure (WSS) hatlarını inceler. Temel işlevi; tarayıcıdan dışa aktarılan HTTP Arşiv (HAR) loglarını bellek korumalı şekilde ayrıştırmak, binary (Opcode 2) Protobuf şemalarını çözmek, Noise el sıkışma (Handshake) durumlarını doğrulamak ve ağ üzerinden akan kritik kimlik bilgilerini avlamaktır.

---

## 2. Protokol ve Mimari Akış Şeması
Analiz motoru, girdi olarak aldığı ham trafik verisini katman katman süzgeçten geçirerek nihai adli bilişim raporuna dönüştürür.

### Veri İşleme Katmanları:
1. **İçeri Alma (Data Ingestion):** JSON formatındaki HAR verisi, büyük dosya korumalı `errors='ignore'` süzgeciyle okunur.
2. **Paket Dilimleme (Slicing):** İstekler HTTP endpointleri ve WebSocket frame'leri olarak ikiye ayrılır.
3. **Kripto Doğrulama (Crypto Verification):** Paket bütünlüğü, Shannon Entropi ve Byte frekans matrisleri üzerinden matematiksel teste tabi tutulur.
4. **Binary De-serialization:** İkili paketler (Opcode 2) Protobuf tel tiplerine (Wire Types) ve alan numaralarına (Field Numbers) göre parçalanır.
5. **Tehdit Avcılığı (DPI):** RegEx imza kütüphanesiyle hassas veriler, oturum token'ları (JWT) ve enjeksiyon anomali desenleri taranır.

---

## 3. Algoritma ve Durum Makinesi (FSM) Mantığı
WhatsApp Web, bağlantı başlangıcında `Noise_XX_25519_AESGCM_SHA256` şeması uyarınca el sıkışır. Geliştirilen modül, bu kriptografik tünel durumlarını takip etmek için bir **Sonlu Durum Makinesi (Finite State Machine)** simüle eder.

### Protokol Durum Geçişleri:
* **`UNINITIALIZED`:** Tünel henüz kurulmadı. Ağ üzerinden Opcode 1 (Text) formatında "noise_handshake" deseni beklenir.
* **`NOISE_HANDSHAKE_START`:** İstemcinin el sıkışma niyetini beyan ettiği aşamadır.
* **`NOISE_HANDSHAKE_SENT`:** İstemci tarafında üretilen Curve25519 Ephemeral Public Key nesnesi karşı tarafa gönderildiğinde bu duruma geçilir.
* **`AUTHENTICATED`:** Sunucu el sıkışma parametrelerini doğrulayıp HKDF (HMAC-based Key Derivation Function) ile Chaining Key ve Cipher Key türetimini onayladığında tünel güvenli hale gelir.
* **`SESSION_ESTABLISHED`:** WhatsApp Web'in ana senkronizasyon paketleri (Ready / Presence) başarıyla geçtiğinde oturum tam kalıcılığa ulaşır.
* **`TERMINATED`:** "Goodbye" veya bağlantı kopma frame'i yakalandığında durum makinesi sonlanır.

---

## 4. Kriptografik ve Ofansif Analiz Parametreleri

### A. Shannon Entropi Süzgeci
Verinin rastarasallık (randomness) derecesi şu formülle hesaplanır:
$$H(X) = -\sum_{i=1}^{n} P(x_i) \log_2 P(x_i)$$

* **$H(X) \ge 7.5$:** Paket yüksek ihtimalle Noise tünelinde şifrelenmiştir veya binary medyadır.
* **$H(X) \le 4.5$:** Paket düz metindir (Plaintext JSON/XML). Siber güvenlik açısından sızıntı kaynağı olma riski taşır.

### B. Ofansif Fuzzing ve Replay Simülatörü
* **Bit-Flipping Atağı:** Yakalanan paket verisinin ilk karakteri üzerinde `XOR 0xFF` işlemi gerçekleştirilerek paket yapısı bozulur ve protokol bütünlük (MAC) doğrulama mekanizmasının mukavemeti ölçülür.
* **Token Hijack Replay:** DPI motoru tarafından yakalanan session token'ları veya JWT mimarileri, düşük entropili paket frame'lerinin içine enjekte edilerek yetkisiz oturum çalma simülasyonu yürütülür.

---

## 5. Kurulum, Entegrasyon ve Test Senaryoları

### Alt Motor Entegrasyonu
Ana `WhatsAppRepositoryAnalyzer` sınıfı, iş yükünü dağıtmak ve modüler kod hacmini (Code Volume) artırmak için şu iki alt sınıfla asenkron mantıkla konuşur:
* `WhatsAppProtobufDecoder` (`src/core/protobuf.py`): İkili verileri çözer.
* `WhatsAppNoiseHandshakeSimulator` (`src/core/crypto_handshake.py`): Kriptografik durumları yönetir.

### Manuel Test Komutu
```bash
python src/main.py --har data/traffic.har --output reports/analysis-report.md --fuzz-index 0

### Docker İzolasyon Komutu
Konteyner mimarisini izole ağ modunda başlatmak için terminalde şu komut koşturulur:

docker compose up --build

---

## 6. Bilinen Kısıtlamalar ve Gelecek Geliştirmeler
* **Canlı Trafik (Live Hooking):** Bu modül statik HAR analizi üzerine kuruludur. Canlı trafiğe anlık müdahale etmek ve bellek manipülasyonu gerçekleştirmek için gelecek fazlarda Frida dynamic instrumentation scriptlerinin ve hooking altyapısının core motorla entegre edilmesi planlanmaktadır.
* **Decryption Sınırı:** Yüksek entropili şifreli paketlerin ($H(X) \ge 7.5$) yapısal bütünlüğü, opcode dağılımları ve paket boyutları analiz edilebilir. Ancak sunucu tarafındaki özel anahtarlar (private keys) izole olduğu için paket içeriği tamamen deşifre edilemez; bu durumlarda risk tahminleme ve anomali skoru modelleri işletilir.

---
> *Bu teknik dokümantasyon, İstinye Üniversitesi BGT210 final projesi kapsamında, siber güvenlik dökümantasyon standartlarına tam uyumlu olarak üretilmiştir.*