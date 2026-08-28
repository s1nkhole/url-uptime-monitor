# URL Uptime Monitor

Сервис, который следит за доступностью списка URL: раз в N секунд
опрашивает их и сохраняет, отвечает сайт или нет.

## Что внутри

- REST API на FastAPI — добавление адресов для мониторинга, просмотр
  статуса и истории проверок
- фоновый поток, который опрашивает все адреса по расписанию
- логи в JSON
- метрики в формате Prometheus + дашборд Grafana
- Docker, Docker Compose, CI на GitHub Actions (lint + тесты), базовый
  Terraform-файл для деплоя на облачный сервер

## Быстрый старт

```bash
git clone <repo-url> && cd url-uptime-monitor
docker compose up -d
```

- API: http://localhost:8000/docs
- Grafana: http://localhost:3000 (admin/admin)
- Prometheus: http://localhost:9090

Добавить адрес для мониторинга:

```bash
curl -X POST http://localhost:8000/targets \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

## Локально без Docker

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
uvicorn app.main:app --reload
pytest app/tests -v
```

## Структура

```
url-uptime-monitor/
├── app/                # код сервиса
├── infra/terraform/     # деплой на облачный VM
├── monitoring/          # Prometheus + Grafana
├── docs/                 # SLA.md
├── .github/workflows/    # CI: lint + тесты
├── docker-compose.yml
└── Dockerfile
```

## Документация

- [SLA.md](./docs/SLA.md)

## Что можно доделать

- alerting поверх Prometheus
- реальный деплой на сервер через Terraform + CI

## Лицензия

MIT
