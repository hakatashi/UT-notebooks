TEX=$(shell find . -name '*.tex')
DVI=$(TEX:.tex=.dvi)
PDF=$(TEX:.tex=.pdf)
JPG=$(shell find . -name '*.jpg')
EPS=$(JPG:.jpg=.eps)

all: $(PDF)

eps: $(EPS)

%.dvi: %.tex eps
	# Compile twice to properly compile \label-\ref
	# http://tex.stackexchange.com/a/111281/116656
	cd $(dir $@); uplatex -no-guess-input-enc -kanji=utf8 -synctex=1 $(notdir $<) 0<&-
	cd $(dir $@); uplatex -no-guess-input-enc -kanji=utf8 -synctex=1 $(notdir $<) 0<&-

%.pdf: %.dvi
	cd $(dir $@); dvipdfmx -o $(notdir $@) $(notdir $<) 0<&-

%.bmp: %.jpg
	convert $< bmp2:$@

%.eps: %.bmp
	potrace $< -r 400 -o $@

.PHONY: clean
clean:
	find . -path ./.git -prune -o ! -name "*.pdf" -type f -exec rm -f {} +
