PYTHON ?= python3
export PYTHONPATH := $(CURDIR)/src

.PHONY: validate test lab-1 lab-2 lab-3 demo

validate:
	$(PYTHON) scripts/validate_repository.py

test:
	$(PYTHON) -m unittest discover -s tests -v

lab-1:
	$(PYTHON) -m soc_lab scenarios/01-sensitive-record-access

lab-2:
	$(PYTHON) -m soc_lab scenarios/02-privileged-account-authentication-anomaly

lab-3:
	$(PYTHON) -m soc_lab scenarios/03-kubernetes-production-control-break

demo: validate test lab-1 lab-2 lab-3
