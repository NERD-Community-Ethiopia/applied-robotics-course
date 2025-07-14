.PHONY: help install test lint format security clean docker-build docker-run docs

# Default target
help:
	@echo "Available commands:"
	@echo "  install     - Install dependencies"
	@echo "  test        - Run tests"
	@echo "  lint        - Run linting"
	@echo "  format      - Format code with Black"
	@echo "  security    - Run security checks"
	@echo "  clean       - Clean up temporary files"
	@echo "  docker-build- Build Docker image"
	@echo "  docker-run  - Run with Docker Compose"
	@echo "  docs        - Build documentation"

# Install dependencies
install:
	python -m pip install --upgrade pip
	pip install -r requirements.txt
	pip install -e ".[dev]"
	pre-commit install

# Run tests
test:
	pytest --cov=./ --cov-report=term-missing --cov-report=html

# Run tests with verbose output
test-verbose:
	pytest -v --cov=./ --cov-report=term-missing

# Run specific test categories
test-unit:
	pytest tests/unit/ -v

test-integration:
	pytest tests/integration/ -v

# Run linting
lint:
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=88 --statistics
	mypy . --ignore-missing-imports

# Format code
format:
	black .
	isort .

# Check formatting without making changes
format-check:
	black --check --diff .
	isort --check-only --diff .

# Run security checks
security:
	bandit -r . -f json -o bandit-report.json
	safety check --json --output safety-report.json

# Clean up temporary files
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type f -name ".coverage" -delete
	find . -type f -name "coverage.xml" -delete

# Build Docker image
docker-build:
	docker build -t generative-ai-course .

# Run with Docker Compose
docker-run:
	docker-compose up -d

# Stop Docker Compose
docker-stop:
	docker-compose down

# Build documentation
docs:
	cd docs && make html

# Run all quality checks
quality: format lint test security

# Setup development environment
setup: install format-check lint test

# Student submission validation
validate-submission:
	python scripts/check_submission.py
	python scripts/test_submission.py

# Generate dependency report
dependency-report:
	python scripts/dependency_report.py

# Run pre-commit hooks
pre-commit:
	pre-commit run --all-files

# Update dependencies
update-deps:
	pip install --upgrade -r requirements.txt
	pip freeze > requirements.txt

# Create new week structure
new-week:
	@read -p "Enter week number: " week; \
	mkdir -p lectures/week-$$week; \
	mkdir -p workshops/week-$$week; \
	echo "# Week $$week" > lectures/week-$$week/README.md; \
	echo "# Week $$week Workshop" > workshops/week-$$week/README.md; \
	echo "Created week $$week structure"

# Help with common issues
troubleshoot:
	@echo "Common issues and solutions:"
	@echo "1. Import errors: Run 'make install'"
	@echo "2. Formatting issues: Run 'make format'"
	@echo "3. Test failures: Check test output and fix issues"
	@echo "4. Docker issues: Run 'make docker-stop && make docker-run'"
	@echo "5. Git issues: Check your branch and remote configuration"

# Show project status
status:
	@echo "Project Status:"
	@echo "Python version: $(shell python --version)"
	@echo "Git branch: $(shell git branch --show-current)"
	@echo "Git status: $(shell git status --porcelain | wc -l) files changed"
	@echo "Docker containers: $(shell docker ps -q | wc -l) running" 