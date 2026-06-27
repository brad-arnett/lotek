.PHONY: install dev test clean dist publish

install:
	pip install . --break-system-packages

dev:
	pip install -e ".[dev]"

test:
	python -m pytest tests/

clean:
	rm -rf dist/ build/ *.egg-info lotek.egg-info lotek_run.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -name "*.pyc" -delete

dist: clean
	python -m build

publish: dist
	twine upload dist/*
