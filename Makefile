.PHONY: build run test

build:
	docker-compose build
run:
	docker-compose up --build -d
	docker-compose exec app /venv/bin/python manage.py migrate
	docker-compose exec app /venv/bin/python manage.py update_rates

test:
	docker-compose exec app /venv/bin/python -m pytest
