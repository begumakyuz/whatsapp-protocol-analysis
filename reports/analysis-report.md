# 📑 BGT210 PROTOKOL TERSİNE MÜHENDİSLİK FİNAL RAPORU

## 🏛️ Kurumsal ve Akademik Bilgiler
- **Kurum:** İstinye Üniversitesi (İSU)
- **Dönem:** 2025-2026 Bahar Dönemi (Spring)
- **Ders Kodu ve Adı:** BGT210 - Tersine Mühendislik (Reverse Engineering)
- **Danışman / Instructor:** Keyvan Arasteh
- **Rapor Üretim Zamanı:** 2026-06-10 01:12:01

## 🎯 Hedef ve Kapsam Bilgisi / Target Info
- **Analiz Edilen Protokol Katmanı:** WebSocket Secure (WSS) / HTTP Archive (HAR)
- **Hedef Platform / Servis:** `web.whatsapp.com` (WhatsApp Web Arayüzü)
- **Yakalanan İletişim Noktası (Endpoint):** 1
- **İncelenen Toplam WebSocket Frame:** 7
- **Tespit Edilen Çalışma Oturumu (Working Sessions):** 1 oturum
- **Nihai Protokol Durumu (Final State):** `NOISE_HANDSHAKE_SENT`

## 📊 Kriptografik Trafik Metrikleri ve İstatistikler
- **Toplam Aktarılan Payload Hacmi:** 270 Bayt
- **Kriptografik Sıkılık Oranı (Encryption Ratio):** %0.0
- **Yüksek Entropili Şifreli Frame Sayısı:** 0
- **Düşük Entropili / Plaintext Frame Sayısı:** 7
- **WebSocket Paket Opcode Dağılım Matrisi:**
  - Opcode `1` (Text Frame): 5 adet paket
  - Opcode `2` (Binary Frame): 2 adet paket

## 🚨 Risk Skoru / Risk Score: 100/100

## 🔍 Siber Tehdit Avcılığı ve Bulgular / Findings
### 1. [Kritik] Query Parametresinde veya Paket İçinde Oturum Sızıntısı (Session Leakage)
- **Kanıt ve Gösterge / Evidence:** `DPI Motoru 1 adet ifşa olmuş anahtar dizisi yakaladı.`
- **Zafiyet Azaltma Önerisi / Remediation:** Hassas session veya state token'ları asla URL parametrelerinde veya düz metin olarak aktarılmamalıdır.

### 2. [Orta] Protokol Korumasında Düşük Entropi Kalıntısı (Plaintext Leak)
- **Kanıt ve Gösterge / Evidence:** `WebSocket trafiğinin %100.0'si zayıf kriptografi içeriyor.`
- **Zafiyet Azaltma Önerisi / Remediation:** Trafik Noise Protocol şemasına girmeden önce hiçbir plaintext loglama yapılmamalıdır.

---
> *Bu teknik rapor ve adli bilişim kanıt dökümanı, WP-DRE otomasyon betiği ve QDebugger kuralları çerçevesinde otomatik üretilmiştir.*
