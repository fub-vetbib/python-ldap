# $Id$

PYTHON=	python

all: build

build: .force
	$(PYTHON) setup.py build

install:
	$(PYTHON) setup.py install

dist: .force
	$(PYTHON) setup.py bdist

srcdist: .force
	-mkdir -p dist
	NAME=python-ldap-`$(PYTHON) setup.py --version`; \
	cd dist && \
	rm -rf $$NAME && \
	cvs -d :pserver:anonymous@cvs.python-ldap.sourceforge.net:/cvsroot/python-ldap export -rHEAD -d $$NAME python-ldap && \
	tar fcv - $$NAME | gzip -9 > $$NAME-src.tar.gz

clean:
	$(PYTHON) setup.py clean --all
	-rm -rf dist build

.force: ;
