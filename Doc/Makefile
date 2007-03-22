# $Id$

PYTHONSRC=	/home/michael/src/Python-2.5
DOCTOOLSDIR=	$(PYTHONSRC)/Doc/tools
PAPER=		a4
DVIPS=		dvips -N0 -t $(PAPER)
PYTHON=		python
MKHOWTO=	$(DOCTOOLSDIR)/mkhowto
MKDVI=		$(MKHOWTO) --dvi
MKPDF=		$(MKHOWTO) --pdf
TEXINPUTS=	$(PYTHONSRC)/Doc/texinputs::
ENV=		/usr/bin/env TEXINPUTS=$(TEXINPUTS)

SRCS=python-ldap.tex ldap.tex version.tex ldif.tex ldapurl.tex \
     ldap-async.tex ldap-modlist.tex ldap-schema.tex

all: python-ldap.dvi python-ldap.ps python-ldap.pdf python-ldap/index.html

python-ldap/index.html: $(SRCS)
	$(ENV) $(MKHOWTO) --html python-ldap.tex
python-ldap.ps: python-ldap.dvi
	$(ENV) $(DVIPS) -o python-ldap.ps python-ldap.dvi
python-ldap.dvi: $(SRCS)
	$(ENV) $(MKDVI) python-ldap.tex
python-ldap.pdf: $(SRCS)
	$(ENV) $(MKPDF) python-ldap.tex
version.tex:
	v=`${PYTHON} ../setup.py --version`; \
	d=`date +"%B %e, %Y"`; \
	echo "%release{$$v}%setshortversion{$$v}%date{$$d}" | tr % "\\\\" >$@
clean:
	rm -f *~ *.bck *.aux *.idx *.ilg *.ind *.log *.toc 
	rm -f *.bkm *.syn *.pla *.l2h *.how
	rm -f python-ldap.dvi python-ldap.ps python-ldap.pdf
	rm -f version.tex
	rm -rf python-ldap

