SRC=src
DOCS=docs

ARIA_SRC=$(SRC)/aria
SPHINX_SRC=$(SRC)/sphinx

.PHONY: clean aria-requirements docs-requirements docs

clean:
	rm -rf $(DOCS)

aria-requirements:
	pip install --upgrade --requirement $(ARIA_SRC)/requirements.txt

docs-requirements:
	pip install --upgrade --requirement $(SPHINX_SRC)/requirements.txt

docs: docs-requirements
	sphinx-build -c $(SPHINX_SRC) -b html $(DOCS)
