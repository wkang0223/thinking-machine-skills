.PHONY: validate build

validate:
	python3 scripts/skillpack.py validate

build:
	python3 scripts/skillpack.py build
