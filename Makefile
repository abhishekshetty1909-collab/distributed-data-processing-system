.PHONY: up down logs ps test clean
up:
	docker compose up --build -d
down:
	docker compose down
logs:
	docker compose logs -f producer consumer
ps:
	docker compose ps
test:
	pytest -q
clean:
	docker compose down -v
