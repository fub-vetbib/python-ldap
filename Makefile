# $Id$

PYTHON=	python

all:
	$(PYTHON) setup.py build
install:
	$(PYTHON) setup.py install
clean:
	$(PYTHON) setup.py clean --all
	rm -rf build
