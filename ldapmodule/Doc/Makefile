
# $Id$

TARGET = Doc
SRCS=	$(TARGET).tex constants.tex functions.tex LDAPObject.tex libldap.tex

build:	Doc.ps Doc.pdf

$(TARGET).ps: $(TARGET).dvi
	dvips -o $@ $(TARGET).dvi

$(TARGET).pdf: $(TARGET).ps
	ps2pdf $(TARGET).ps $@

$(TARGET).dvi:	$(SRCS)
	latex $(TARGET)
	latex $(TARGET)

$(TARGET).html: $(SRCS) tex2html
	perl tex2html $(SRCS) >$@

clean:
	rm -f *.aux *.dvi *.idx *.log 

distclean: clean
	rm $(TARGET).ps
