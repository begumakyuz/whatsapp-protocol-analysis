# Temiz, hafif ve güvenli resmi Python imajı
FROM python:3.12-slim

# Konteyner içi çalışma dizini sabitlemesi
WORKDIR /app

# Sistem bağımlılıklarının ve güvenlik güncellemelerinin kurulması
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /lib/apt/lists/*

# Bağımlılıkların optimize edilerek önbelleksiz kurulması
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Proje kaynak kodlarının izole alana kopyalanması
COPY . .

# CLI giriş noktasının tanımlanması
ENTRYPOINT ["python", "src/main.py"]
CMD ["--har", "data/traffic.har"]