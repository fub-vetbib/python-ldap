# $Id$

PYTHONSRC=	/home/michael/src/Python-2.2
DOCTOOLSDIR=	$(PYTHONSRC)/Doc/tools
PAPER=		a4
DVIPS=		dvips -N0 -t $(PAPER)
PYTHON=		python
MKHOWTO=	$(DOCTOOLSDIR)/mkhowto
MKDVI=		$(MKHOWTO) --dvi
MKPDF=		$(MKHOWTO) --pdf
TEXINPUTS=	$(PYTHONSRC)/Doc/texinputs::
ENV=		/usr/bin/env TEXINPUTS=$(TEXINPUTS)

SRCS= lib.tex libldap.tex version.tex

all: lib.dvi lib.ps lib.pdf lib/index.html

lib/index.html: $(SRCS)
	$(ENV) $(MKHOWTO) --html lib.tex
lib.ps: lib.dvi
	$(ENV) $(DVIPS) -o lib.ps lib.dvi
lib.dvi: $(SRCS)
	$(ENV) $(MKDVI) lib.tex
lib.pdf: $(SRCS)
	$(ENV) $(MKPDF) lib.tex
version.tex:
	v=`${PYTHON} ../setup.py --version`; \
	d=`date +"%B %e, %Y"`; \
	echo "%release{$$v}%setshortversion{$$v}%date{$$d}" | tr % "\\\\" >$@
clean:
	rm -f *~ *.aux *.idx *.ilg *.ind *.log *.toc 
	rm -f *.bkm *.syn *.pla *.l2h *.how
	rm -f lib.dvi lib.ps lib.pdf
	rm -f version.tex
	rm -rf lib

upload:
	scp -r -C lib.ps lib.pdf lib shell.sourceforge.net:htdocs/doc/
