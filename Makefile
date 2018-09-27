.PHONY: build run test

build:
	docker-compose build

run:
	docker-compose run

test:
	docker-compose run app /venv/bin/python -m pytest
