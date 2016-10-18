TEX=$(shell find . -name '*.tex')
DVI=$(TEX:.tex=.dvi)
PDF=$(TEX:.tex=.pdf)

%.dvi: %.tex
	uplatex -no-guess-input-enc -kanji=utf8 -synctex=1 -output-directory=$(dir $@) $< 0<&-

%.pdf: %.dvi
	dvipdfmx -o $@ $< 0<&-

all: $(PDF)
