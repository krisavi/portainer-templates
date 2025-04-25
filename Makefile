.PHONY: all install_requirements download combine

PYTHON := $(shell which python3 2>/dev/null || which python)

all: install_requirements download combine convertv2 list

install_requirements:
	"$(PYTHON)" -m pip install -r lib/requirements.txt

download:
	"$(PYTHON)" lib/download.py

combine:
	"$(PYTHON)" lib/combine.py

convert:
	"$(PYTHON)" lib/convert.py

convertv2:
	"$(PYTHON)" lib/convertv2.py

validate:
	"$(PYTHON)" lib/validate.py

validatev3:
	"$(PYTHON)" lib/validate_v3.py

list:
	"$(PYTHON)" lib/list.py
