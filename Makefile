.PHONY: check build test clean index ask

check:
	python scripts/normalize_encoding.py
	python scripts/validate_docs.py
	python scripts/validate_adrs.py
	python scripts/check_links.py
	pytest -q

build:
	mkdocs build --strict

test:
	pytest -q

index:
	python scripts/build_index.py

ask:
	python scripts/ask.py "$(Q)"

clean:
	rm -rf site .pytest_cache **/__pycache__ index
