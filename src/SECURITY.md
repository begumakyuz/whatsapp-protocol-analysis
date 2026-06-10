# Security Policy (🛡️ Güvenlik Politikası)

## Proje Kapsamı (Scope)
Bu framework, tamamen eğitim, araştırma ve siber güvenlik adli bilişim (forensics) süreçlerini simüle etmek amacıyla geliştirilmiş akademik bir çalışmadır. Canlı sistemleri, WhatsApp sunucularını veya aktif kullanıcı trafiğini manipüle etme, kırma veya sabote etme yeteneğine sahip değildir.

## Sorumlu Açıklama (Responsible Disclosure)
Eğer bu simülasyon mantığında veya kod tabanında bir mantık hatası ya da zafiyet tespit ederseniz, lütfen doğrudan bir GitHub Issue açmak yerine geliştirici ile özel iletişim kanalları üzerinden irtibata geçiniz.

## Bilinen Sınırlar (Known Limitations)
1. Kriptografik anahtar değişim süreçleri adli analiz akışını doğrulamak adına simüle edilmiştir (Mock Key Exchange).
2. Canlı ağ soketlerine müdahale edilmez; statik `.har` logları üzerinde parser simülasyonu koşturulur.