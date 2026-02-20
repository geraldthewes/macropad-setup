DEVICE_ID := 5633
PYTHON := .venv/bin/python

.PHONY: install print compile

install:
	bash macropad.sh

print:
	vitaly -i $(DEVICE_ID) layers -p

compile:
	$(PYTHON) compile_macropad.py examples/current-emacs.yaml
