# Makefile
# Load environment variables from .env file
include .env.development
export $(shell sed 's/=.*//' .env.development)

# Export requirements into a file
.PHONY: req
make req:
	pip freeze > requirements.txt

# Define Docker image name
IMAGE_NAME=tt-postgres:latest

# Define container name
CONTAINER_NAME=$(DEV_CONTAINER_NAME)

# Build Docker image, create and run the container, initialize the database, and export connection info
.PHONY: build-dev-db
build-dev-db:
	@echo "Building Docker image..."
	docker build --build-arg POSTGRES_USER=$(POSTGRES_USER) \
                 --build-arg POSTGRES_PASSWORD=$(POSTGRES_PASSWORD) \
                 --build-arg POSTGRES_DB=$(POSTGRES_DB) \
                 -t $(IMAGE_NAME) .
	@echo "Running Docker container..."
	docker run -d --name $(CONTAINER_NAME) -p 5432:5432 \
		-v $(VOLUME_NAME):/var/lib/postgresql/data \
		$(IMAGE_NAME)
	@echo "Waiting for PostgreSQL to start..."
	@until docker exec $(CONTAINER_NAME) pg_isready -U $(POSTGRES_USER) -d $(POSTGRES_DB); do \
		echo "Waiting for PostgreSQL to be ready..."; \
		sleep 2; \
	done
	@echo "Initializing the database with SQL script..."
	docker exec -i $(CONTAINER_NAME) psql -U $(POSTGRES_USER) -d $(POSTGRES_DB) -f /docker-entrypoint-initdb.d/tt_postgres_setup.sql
	@echo "Exporting database connection details..."
	@echo "Database connection details:"
	@echo "Host: localhost"
	@echo "Port: 5432"
	@echo "User: $(POSTGRES_USER)"
	@echo "Password: $(POSTGRES_PASSWORD)"
	@echo "Database: $(POSTGRES_DB)"

# Stop and remove the Docker container
.PHONY: stop-container
stop-container:
	@echo "Stopping and removing Docker container..."
	-docker stop $(CONTAINER_NAME)
	-docker rm $(CONTAINER_NAME)

# Remove the Docker volume
.PHONY: remove-volume
remove-volume:
	@echo "Removing Docker volume..."
	-docker volume rm $(VOLUME_NAME)

# Clean up both container and volume
.PHONY: clean
clean:
	@make stop-container
	@make remove-volume

# Pre-commit
.PHONY: pre
pre:
	@echo "Running pre-commit..."
	pre-commit run --all-files
