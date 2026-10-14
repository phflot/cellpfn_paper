.PHONY: all pdf check words tables index
all: pdf check

pdf:
	python3 scripts/build_pdf.py

tables:
	python3 scripts/build_tables.py

index:
	python3 scripts/index_export.py

words:
	python3 scripts/count_words.py

check:
	python3 scripts/verify.py
