# $Id$

DOCTOOLSDIR=	/usr/obj/ports/lang/python-threads/Python-2.0/Doc/tools
PAPER=		a4
DVIPS=		dvips -N0 -t $(PAPER)
PYTHON=		python
MKHOWTO=	$(DOCTOOLSDIR)/mkhowto
MKDVI=		$(MKHOWTO) --dvi
MKPDF=		$(MKHOWTO) --pdf

SRCS=	lib.tex libldap.tex

all: lib.dvi lib.ps lib.pdf lib.html 

lib.html: $(SRCS)
	$(MKHOWTO) --html lib.tex
lib.ps: lib.dvi
	$(DVIPS) -o lib.ps lib.dvi
lib.dvi: $(SRCS)
	$(MKDVI) lib.tex
lib.pdf: $(SRCS)
	$(MKPDF) lib.tex
clean:
	rm -f *~ *.aux *.idx *.ilg *.ind *.log *.toc 
	rm -f *.bkm *.syn *.pla *.l2h *.how
	rm -f lib.dvi lib.ps lib.pdf
	rm -rf lib
