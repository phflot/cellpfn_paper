.PHONY: all pdf check words tables index figure figures
all: pdf check

pdf:
	python3 scripts/build_pdf.py

figure:
	python3 scripts/build_architecture.py

tables:
	python3 scripts/build_tables.py

index:
	python3 scripts/index_export.py

words:
	python3 scripts/count_words.py

check:
	python3 scripts/verify.py

figures:
	python3 scripts/build_figures.py
