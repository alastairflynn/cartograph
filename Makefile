build: setup.py
	python setup.py sdist bdist_wheel

.PHONY: upload
upload:
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

.PHONY: docs
docs:
	cd ./docs && $(MAKE) html

.PHONY: clean
clean:
	rm dist/*

all:
	build
