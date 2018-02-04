# Makefile to run setup.py

install:
	python setup.py install

clean:
	python setup.py clean

docs:
	python setup.py docs

build:
	python setup.py build

bdist:
	python setup.py bdist

dist:
	python setup.py dist

test:
	python setup.py test