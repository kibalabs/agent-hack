install:
	@ pip install -r requirements.txt -r requirements-dev.txt

list-outdated: install
	@ pip list -o

lint-check:
	@ lint-check *.py ./carlistings

lint-check-ci:
	@ lint-check *.py ./carlistings --output-file lint-check-results.json --output-format annotations

lint-fix:
	@ isort --sl -l 1000 *.py ./carlistings
	@ lint-check *.py ./carlistings

type-check:
	@ type-check *.py ./carlistings

type-check-ci:
	@ type-check *.py ./carlistings --output-file type-check-results.json --output-format annotations

security-check:
	@ security-check *.py ./carlistings

security-check-ci:
	@ security-check *.py ./carlistings --output-file security-check-results.json --output-format annotations

build:
	@ echo "Not Supported"

start:
	@ uvicorn application:app --host 0.0.0.0 --port 5000 --no-access-log --reload

start-prod:
	@ uvicorn application:app --host 0.0.0.0 --port 5000 --no-access-log

test:
	@ echo "Not Supported"

clean:
	@ rm -rf ./.mypy_cache ./__pycache__ ./build ./dist

.PHONY: *
