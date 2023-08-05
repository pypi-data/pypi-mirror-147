# Makefile for unit tests.

include ../conf/config.mk

PKG    = makexlsx
RUN    = $(PYTHON) -m pytest $(OPTS) $(ARGS)
COVER  = --cov $(PKG) --cov-config=$(CFG) $(addprefix --cov-report , $(REPORT))
PROF   = --profile
CFG    = coverage.cfg
REPORT = term html

CLEANFILES = .coverage htmlcov prof __pycache__ *.xlsx

.DEFAULT:; @ $(MAKE) test TEST=test-$@.py

all: help

test: ## Run tests
	$(RUN) $(TEST)

cover: ## Run tests with coverage
	$(RUN) $(COVER) $(TEST)

profile: ## Run tests with profiling
	$(RUN) $(PROF) $(TEST)

clean: ## Clean up
	rm -rf $(CLEANFILES)
