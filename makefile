# Proje Otomasyon ve Kısayol Yönetimi

.PHONY: install run docker-build docker-run clean

# Bağımlılıkları yerel ortama kurar
install:
	pip install -r requirements.txt

# Analiz motorunu yerelde test HAR dosyası ile çalıştırır
run:
	python src/main.py --har data/traffic.har

# Docker imajını derler
docker-build:
	docker compose build

# Docker üzerinde analiz hattını tetikler
docker-run:
	docker compose run --rm analyzer

# Önbellek ve kalıntı dosyaları sistemden temizler
clean:
	rm -rf __pycache__ src/core/__pycache__ .pytest_cache
	find . -type d -name "__pycache__" -exec rm -r {} +