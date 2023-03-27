# Build package
.PHONY: build
build:
	python setup.py sdist bdist_wheel

# Upload package to PyPI
.PHONY: upload
upload: build
	python -m twine upload dist/* --skip-existing