all: 
	docker compose -f docker/docker-compose.yml --project-directory . up --build -d
	poetry run alembic upgrade head;
	



