# Makefile for Mallku ICML 2025 Poster
# Compile with: make

LATEX = xelatex
POSTER = mallku-icml-poster-expanded

all: $(POSTER).pdf

$(POSTER).pdf: $(POSTER).tex
	$(LATEX) $(POSTER).tex
	$(LATEX) $(POSTER).tex  # Run twice for references

clean:
	rm -f $(POSTER).aux $(POSTER).log $(POSTER).out $(POSTER).pdf

preview: $(POSTER).pdf
	@echo "PDF generated! Open $(POSTER).pdf to preview"

.PHONY: all clean preview
