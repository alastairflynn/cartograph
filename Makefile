build: setup.py
	python setup.py sdist bdist_wheel

upload:
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

clean:
	rm dist/*

all:
	build
