.PHONY: all pdf check words
all: pdf check

pdf:
	mkdir -p build output/review
	latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex
	cp build/main.pdf output/cellpfn_wave1.pdf

words:
	python3 scripts/count_words.py

check:
	python3 scripts/verify.py
