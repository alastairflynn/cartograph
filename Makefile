build: setup.py
	python setup.py sdist bdist_wheel

all:
	build

clean:
	rm dist/*
