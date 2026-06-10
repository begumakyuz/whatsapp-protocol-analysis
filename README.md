<div align="center">
  <a href="https://istinye.edu.tr">
    <img src="https://upload.wikimedia.org/wikipedia/commons/7/7c/Istinye_University_Logo.png" alt="İstinye Üniversitesi" width="180"/>
  </a>

  # 🛡️ WhatsApp Web Network Protocol Forensic & Offensive Security Analyzer 🚀

  ![GitHub](https://img.shields.io/badge/GitHub-Private-red?style=flat-square&logo=github)
  ![Dil](https://img.shields.io/badge/Dil-Python-blue?style=flat-square&logo=python)
  ![Durum](https://img.shields.io/badge/Durum-Devam%20Ediyor-yellow?style=flat-square&logo=git)
  ![Ders](https://img.shields.io/badge/Ders-BGT210-purple?style=flat-square)
</div>

---

## 👨‍🏫 Danışman Bilgisi
| Özellik | Açıklama |
| :--- | :--- |
| **Ad Soyad** | Keyvan Arasteh |
| **GitHub** | [@keyvanarasteh](https://github.com/keyvanarasteh) |
| **E-posta** | keyvan.arasteh@istinye.edu.tr |
| **LinkedIn** | [keyvanarasteh](https://linkedin.com/in/keyvanarasteh) |
| **Web Sitesi** | [qline.tech](https://qline.tech) |

## 👩‍💻 Öğrenci Bilgisi
| Özellik | Açıklama |
| :--- | :--- |
| **Ad Soyad** | Begüm Akyüz |
| **Öğrenci No** | 2420****1005 |

## 📚 Ders Bilgileri
| Özellik | Açıklama |
| :--- | :--- |
| **Ders Adı** | Tersine Mühendislik Giriş / İleri Ağ Güvenliği |
| **Ders Kodu** | BGT210 |
| **Kredi** | 4 AKTS |
| **Ön Koşullar** | Python CLI, Wireshark, Ağ Temelleri, Kriptografi Giriş |
| **Dönem** | 2025-2026 Bahar |

---

## 🎯 1. Proje Özeti ve Kapsamı
Bu framework, `web.whatsapp.com` (WhatsApp Web) arabiriminin kapalı devre ağ katmanı protokol yapısını tersine mühendislik süzgecinden geçirir. Tarayıcı DevTools paneli üzerinden dışa aktarılan ham HTTP Arşiv (**HAR**) verilerini asenkron olarak süzerek WebSocket Secure (WSS) tünel kanallarındaki ikili verileri (Binary Frames) parse eder ve güvenlik açıklarına karşı denetler. 🕵️‍♂️🛡️

---

## ⚙️ 2. Sistem Mimarisi (Architecture Flow)

Projenin veri işleme, analiz ve raporlama hattı aşağıdaki mimari hiyerarşiyi takip etmektedir:

```text
[ 📂 Ham HAR Dosyası ]
        │
        ▼
[ 🔍 Core HAR Parser ] ───► (Filtreleme: resourceType == "websocket")
        │
        ▼
[ 🧪 WSS Frame Extractor ] ───► (Opcode Ayrıştırma: Text vs Binary Frame)
        │
        ▼
[ 🧠 Protocol Analyzer Core ]
        ├──► 📊 Shannon Entropy Analizörü (Kriptografik Doğrulama)
        ├──► ⚙️ Finite State Machine (Handshake Durum Takibi)
        └──► 🎛️ Low-Level Protobuf Decoder (Varint/Wire Type Sökücü)
        │
        ▼
[ 💥 Offensive Fuzzing Simulator ] ───► (Bit-Flipping Mutation & Replay Attack)
        │
        ▼
[ 📝 Automated Report Generator ] ───► (Diske analysis-report.md Çıktısı)

🧠 3. Teknik Derinlik ve Gerçek İmplementasyon Eşleşmesi

Kaynak kod içerisindeki matematiksel ve mantıksal fonksiyonlar, dökümantasyonda beyan edilen siber güvenlik senaryolarıyla %100 uyumludur:

    📊 Shannon Entropy Analizörü (calculate_shannon_entropy): Paket verilerinin matematiksel entropi ve byte frekans matrisini çıkartarak, trafiğin düz metin mi yoksa Noise Protocol şemalarıyla mı şifrelendiğini matematiksel olarak doğrular.

    ⚙️ Finite State Machine (track_fsm_state): WhatsApp Web el sıkışma (Handshake) adımlarını ve geçici anahtar (Ephemeral Key) değişim durumlarını kronolojik indeksler üzerinden anlık takip eder.

    🎛️ Protobuf Binary Decoder (decode_varint & parse_wire_type): Opcode 2 (Binary Frame) olan ikili paketleri, harici kütüphane bağımlılığı olmadan tel tiplerine (Wire Type) ve alan numaralarına (Field Number) göre de-serialize eder.

    💥 Ofansif Fuzzing Simülatörü (simulate_offensive_fuzzing): Paket yapılarını bozarak (Bit-Flipping) veya token enjeksiyonu (Replay Attack) yaparak protokolün mukavemet sınırlarını izole sandbox üzerinde test eder.

📋 Örnek JSON Analiz Çıktısı (Mock Stream Output)
JSON

{
  "protocol": "Noise_XX_25519_AESGCM_SHA256",
  "encrypted": true,
  "calculated_entropy": 7.92,
  "current_fsm_state": "NOISE_HANDSHAKE_SENT",
  "fuzzing_telemetry": {
    "bit_flipping_response": "400_Bad_Request_MAC_Failed",
    "replay_attack_vulnerable": true
  }
}

📂 4. Repository Klasör Yapısı
<pre><code>.
├── 🛠️ .github/
│   └── 🤖 workflows/
│       └── 🧪 ci.yml
├── 📊 data/
│   └── 📥 traffic.har
├── 📚 docs/
│   ├── 🧩 modules/
│   │   └── 📄 websocket-parser.md
│   ├── 🔗 references/
│   │   └── 📄 links.md
│   └── 🔬 research/
│       └── 📄 research-notes-template.md
├── 📝 reports/
│   └── 📄 analysis-report.md
├── 🗃️ src/
│   ├── 🧠 core/
│   │   ├── 🐍 crypto_handshake.py
│   │   ├── 🐍 parser.py
│   │   └── 🐍 protobuf.py
│   ├── ⚙️ utils/
│   └── 🐍 main.py
├── 🧪 tests/
│   └── 🐍 test_engine.py
├── 📄 .env.example
├── 🛡️ .gitignore
├── 🐳 docker-compose.yml
├── 🐳 Dockerfile
├── 📄 LICENSE
├── 🛠️ makefile
├── 📄 README.md
├── 📋 requirements.txt
└── 🗺️ ROADMAP.md</code></pre>
🧪 5. Kurulum ve Otomatik Test Talimatları
🤖5.1. Sanal Ortam Kurulumu ve Bağımlılıklar
Projenin bağımlılıklarını izole bir tünelde çalıştırmak için öncelikle bir sanal ortam (`venv`) oluşturup aktif etmeniz ve ardından gerekli kütüphaneleri yüklemeniz gerekmektedir:

# 1. Proje ana dizinine gidin
cd whatsapp-protocol-analysis

# 2. Sanal ortamı (venv) oluşturun
python -m venv venv

# 3. Sanal ortamı aktif edin (Windows Git Bash için)
source venv/Scripts/activate

# 4. Bağımlılıkları ve test motorunu (pytest) yükleyin
pip install -r requirements.txt pytest
🧪 5.2. Otomatik Ünite Testleri (PyTest & CI/CD)

Yazdığımız düşük seviyeli Protobuf Varint decoder modülleri, Shannon entropi hesaplama algoritmaları ve FSM durum geçişleri için hazırlanan test paketlerini yerelde çalıştırmak için:
Bash

# Tüm test senaryolarını detaylı log çıktısıyla koşturun
pytest -v

Not: Bu test hattı, reponun kök dizininde yer alan .github/workflows/ci.yml sayesinde GitHub'a her push yaptığınızda otomatik olarak bulutta da tetiklenmektedir.
💻 5.3. Yerel Adli Analiz Hattını Çalıştırma (Forensic Pipeline)

Yerel bilgisayarınızda bulunan ham ağ paketi verisini (data/traffic.har) siber güvenlik motoruna salıp, otomatik kurumsal adli rapor üretmek için:
Bash

# Sanal ortam aktifken analiz motorunu ateşleyin
python src/main.py --har data/traffic.har

İşlem tamamlandığında, analiz sonuçları ve ofansif fuzzing metrikleri otomatik olarak reports/analysis-report.md dosyasına kurumsal Markdown formatında yazılacaktır.
🐋 5.4. Docker Laboratuvar İzolasyon Testi

Bağımlılıklar veya işletim sistemi farklılıklarından tamamen izole, temiz bir Docker Sandbox üzerinde tüm analiz hattını ayağa kaldırmak için:
Bash

# Docker imajını derleyin ve izole konteyneri ayağa kaldırın
docker compose up --build

    ⚠️ Bu proje, siber güvenlik dökümantasyon ve adli bilişim standartlarına tam uyumlu, otomatik test (CI/CD) altyapısına sahip açık kaynaklı bir portföy çalışmasıdır. 🕵️‍♂️💎