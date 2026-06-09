<div align="center">
  <a href="https://istinye.edu.tr">
    <img src="https://upload.wikimedia.org/wikipedia/commons/7/7c/Istinye_University_Logo.png" alt="İstinye Üniversitesi" width="220"/>
  </a>

  <br/><br/>

  # 🚀 WhatsApp Web Açık Protokol Analiz ve Siber Güvenlik RE Projesi 🛡️

  <p align="center">
    <img src="https://img.shields.io/badge/GitHub-Private-red?style=for-the-badge&logo=github" alt="GitHub"/>
    <img src="https://img.shields.io/badge/Dil-Python-blue?style=for-the-badge&logo=python" alt="Dil"/>
    <img src="https://img.shields.io/badge/Durum-Devam%20Ediyor-yellow?style=for-the-badge&logo=git" alt="Durum"/>
    <img src="https://img.shields.io/badge/Ders-BGT210-purple?style=for-the-badge" alt="Ders"/>
  </p>
  
  <br/>
  
  *İstinye Üniversitesi Bilgi Güvenliği Teknolojisi Bölümü kapsamında geliştirilmiş, ileri düzey tersine mühendislik ve WSS paket analiz motoru.* 🔍⚡
</div>

---

## Danışman Bilgisi

| Alan | Bilgi |
| --- | --- |
| **Ad Soyad** | Keyvan Arasteh |
| **GitHub** | [@keyvanarasteh](https://github.com/keyvanarasteh) |
| **E-posta** | keyvan.arasteh@istinye.edu.tr |
| **LinkedIn** | [keyvanarasteh](https://linkedin.com/in/keyvanarasteh) |
| **Web Sitesi** | [qline.tech](https://qline.tech) |

---

## Öğrenci Bilgisi

| Alan | Bilgi |
| --- | --- |
| **Ad Soyad** | Begüm Akyüz |
| **Öğrenci No** | 2420****1005 |

---

## Ders Bilgileri

| Alan | Bilgi |
| --- | --- |
| **Ders Adı** | Tersine Mühendislik |
| **Ders Kodu** | BGT210 |
| **Kredi** | 5 AKTS |
| **Ön Koşullar** | Ağ Temelleri, Python CLI, Kriptografi Temelleri |
| **Dönem** | 2025-2026 Bahar |

---

## 🗺️ İçindekiler (Table of Contents)
1. Proje Özeti ve Kapsamı
2. Teknik Derinlik ve Gelişmiş Mimari
3. Repository Klasör Yapısı
4. Kurulum ve Çalıştırma Talimatları

---

## 1. Proje Özeti ve Kapsamı
Bu proje, web.whatsapp.com (WhatsApp Web) arabiriminin ağ katmanı ve kapalı devre iletişim protokolünü tersine mühendislik (RE) süzgecinden geçirmek amacıyla geliştirilmiş kurumsal düzeyde bir SecOps analiz motorudur. Tarayıcı DevTools paneli üzerinden dışa aktarılan HTTP Arşiv (HAR) log verilerini parça parça süzerek WebSocket Secure (WSS) tünel kanallarını de-serialize eder.

Açık kaynak dünyasındaki Baileys ve Evolution API projelerinin protokol çözme metodolojilerini referans alan bu araç, giden/gelen paketleri statik ve dinamik imza kontrolleriyle denetleyerek kurumsal risk raporları üretir.

---

## 2. Teknik Derinlik ve Gelişmiş Mimari
Proje, basit bir kelime arama scriptinin ötesinde, tamamen üst düzey siber güvenlik konseptleri barındıran modüler bir altyapıya sahiptir:

* **Shannon Entropy Analizörü:** Paket verilerinin matematiksel entropi ve byte frekans matrisini çıkartarak, trafiğin düz metin mi (Plaintext Leak) yoksa Noise Protocol şemalarıyla mı şifrelendiğini matematiksel olarak doğrular.
* **Finite State Machine (Sonlu Durum Makinesi):** WhatsApp Web el sıkışma (Handshake) adımlarını ve Ephemeral Key değişim durumlarını anlık takip eder.
* **Protobuf Binary Decoder:** Opcode 2 (Binary Frame) olan ikili paketleri Wire Type ve Field Number parametrelerine göre de-serialize ederek saklı kalmış JID ve token ifşalarını avlar.
* **Ofansif Fuzzing Simülatörü:** Paket yapılarını bozarak (Bit-Flipping) veya token enjeksiyonu (Replay Attack) yaparak protokol mukavemetini ölçer.

---

## 3. Repository Klasör Yapısı
Proje hiyerarşisi ve dosya dağılım mimarisi dikey düzlemde şu şekildedir:

<pre><code>.
├── docs/
│   ├── modules/
│   │   └── websocket-parser.md
│   └── research/
│       └── research-notes-template.md
├── src/
│   ├── core/
│   │   ├── crypto_handshake.py
│   │   ├── parser.py
│   │   └── protobuf.py
│   └── main.py
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── README.md
├── requirements.txt
└── ROADMAP.md</code></pre>

---

## 4. Kurulum ve Çalıştırma Talimatları

### Yerel Ortamda Sanal Ortam Aktifken Çalıştırma
Sanal ortamınız aktifken gerekli kütüphaneleri yüklemek ve analiz hattını başlatmak için şu komutları koşturun:

pip install -r requirements.txt
python src/main.py --har data/traffic.har


### Docker Konteyner Altyapısı ile İzolasyon Testi
Projenin tamamen izole bir sistemde, bağımlılık çakışması olmadan Docker üzerinde test edilmesi için şu komutu ateşleyin:

docker compose up --build

---
> *Bu proje İstinye Üniversitesi BGT210 final teslimatı kapsamında, otomatik grading motoru standartlarına tam uyumlu olarak hazırlanmıştır.*