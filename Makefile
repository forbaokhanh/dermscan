# Makefile for ingredient-scanner

# Variables
PROJECT_NAME = ingredient-scanner
DATA_FILE_PATH = "$(DEV_DIR)/$(PROJECT_NAME)/data/product_info.csv"
DATA_DEST_PATH = "./data/"

# Phony targets to avoid conflicts
.PHONY: build run test fmt pub dist

# Build the application
build:
	poetry run pyinstaller --add-data $(DATA_FILE_PATH):$(DATA_DEST_PATH) --onefile src/main.py

# Run the application
run:
	poetry run python src/main.py

# Run tests
test:
	poetry run pytest tests/

# Format code
fmt:
	poetry run isort . && poetry run black .

# Publish the application
pub:
	sudo mv ./dist/main /usr/local/bin/scan-ingredients

# Build and publish the application
dist: build pub
