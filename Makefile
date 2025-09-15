# We need to tell make that those targets are not backed by real files'
.PHONY: lint fmt format

lint: ## Run code linters
	poetry run ruff check rosbag_splitter.py

fmt format: ## Run code formatters
	poetry run ruff format rosbag_splitter.py
	poetry run ruff check --fix rosbag_splitter.py
