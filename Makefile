VENV_NAME = imap_venv
PYTHON = $(VENV_NAME)/bin/python
PIP = $(VENV_NAME)/bin/pip


.PHONY: clean install run

clean:
	rm -rf $(VENV_NAME)
	rm -rf __pycache__

install:
	python3 -m venv $(VENV_NAME)
	 . $(VENV_NAME)/bin/activate

run:
	$(PYTHON) main.py