TEX=$(shell find . -type f -name '*.tex' -printf '%P\n')
DVI=$(TEX:.tex=.dvi)
PDF=$(addprefix dist/,$(TEX:.tex=.pdf))
IMAGES=$(shell find . -type f \( -name '*.jpg' -or -name '*.png' \) -printf '%P\n')
IMAGES_0=$(IMAGES:.png=.eps)
EPS=$(IMAGES_0:.jpg=.eps)

all: $(EPS) $(PDF)

.INTERMEDIATE: $(DVI)
%.dvi: %.tex images-timestamp.txt
	# Compile twice to properly compile \label-\ref
	# http://tex.stackexchange.com/a/111281/116656
	cd $(dir $@); uplatex -no-guess-input-enc -kanji=utf8 -synctex=1 $(notdir $<) 0<&-
	cd $(dir $@); uplatex -no-guess-input-enc -kanji=utf8 -synctex=1 $(notdir $<) 0<&-

dist/%.pdf: %.dvi
	cd $(dir $<); dvipdfmx -o $(notdir $@) $(notdir $<) 0<&-
	mkdir -p $(dir $@)
	mv $(dir $<)/$(notdir $@) $(dir $@)

.SECONDEXPANSION:
%.bmp: $$(wildcard %.jpg) $$(wildcard %.png)
	@if [ -e "$*.jpg" ]; then convert "$*.jpg" bmp2:$@; else convert "$*.png" bmp2:$@; fi;

%.eps: %.bmp
	potrace $< -r 400 -o $@

.PHONY: clean
clean:
	find . -path ./.git -prune -o ! -name "*.pdf" -type f -exec rm -f {} +
