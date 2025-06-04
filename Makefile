.PHONY: install run test lint format migrate

install:
	poetry install

run:
	poetry run uvicorn app.main:app --reload

test:
	poetry run pytest

lint:
	poetry run flake8 .
	poetry run mypy .

format:
	poetry run black .
	poetry run isort .

migrate:
	poetry run alembic upgrade head

migrate-create:
	poetry run alembic revision --autogenerate -m "$(message)"

docker-build:
	docker-compose build

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f 