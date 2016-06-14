SRC=src
DOCS=docs

ARIA_SRC=$(SRC)/aria
SPHINX_SRC=$(SRC)/sphinx

.PHONY: clean aria-requirements docs-requirements docs

clean:
	rm -rf $(DOCS) out .tox .coverage
	find . -type d -name '*.egg-info' | xargs rm -r
	find . -type d -name '.coverage' | xargs rm -r

aria-requirements:
	pip install --upgrade --requirement $(ARIA_SRC)/requirements.txt

docs-requirements:
	pip install --upgrade --requirement $(SPHINX_SRC)/requirements.txt

docs: docs-requirements
	rm -rf $(DOCS)
	sphinx-build -b html -c $(SPHINX_SRC) $(ARIA_SRC) $(DOCS)

test-requirements:
	pip install --upgrade tox==1.6.1

test: test-requirements
	tox
