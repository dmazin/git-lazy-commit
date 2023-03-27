# Build package
.PHONY: build
build:
	rm -rf dist/*
	python setup.py sdist bdist_wheel

# Upload package to PyPI
.PHONY: upload
upload: build
	python -m twine upload dist/* --skip-existing

# Install main requirements
.PHONY: install
install:
	pip install -r requirements.txt

# Install development requirements
.PHONY: install-dev
install-dev:
	pip install -r requirements-dev.txt
