# $Id$

PYTHON=	python

all:
	$(PYTHON) setup.py build
install:
	$(PYTHON) setup.py install
dist:
	$(PYTHON) setup.py bdist
clean:
	$(PYTHON) setup.py clean --all
	-rmdir build
