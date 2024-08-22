# Makefile
.PHONY: req
make req:
	pip freeze > requirements.txt
