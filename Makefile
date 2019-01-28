# Makefile to run setup.py

install:
	python3 setup.py install

clean:
	python3 setup.py clean

docs:
	python3 setup.py docs

build:
	python3 setup.py build

bdist:
	python3 setup.py bdist

dist:
	python3 setup.py dist

test:
	python3 setup.py test
