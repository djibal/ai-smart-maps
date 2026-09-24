check:
	python scripts/normalize_encoding.py
	python scripts/validate_docs.py
	python scripts/validate_adrs.py
	python scripts/check_links.py
	pytest -q
