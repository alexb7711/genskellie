################################################################################
# Variables
################################################################################

##==============================================================================
# Directories
SRC_D     = src
TST_D     = tests
ENV_DIR   = .venv

##==============================================================================
# File Paths

ifeq ("$(OS)", "Windows_NT")
BIN     = $(ENV_DIR)/Scripts
else
BIN     = $(ENV_DIR)/bin
endif
PYTHON  = python

##==============================================================================
# Makefile configuration
.PHONY: all setup install update run debug clean test help doc

################################################################################
# Recipes
################################################################################

##==============================================================================
#
all: setup update run ## Default action

##==============================================================================
#
install: ## Install genskellie locally
	pip install --user --break-system-packages -e .

##==============================================================================
#
uninstall: ## Uninstall genskellie
	pip uninstall --break-system-packages genskellie

##==============================================================================
#
update: ## Re-install genskellie
	pip install --user --upgrade --break-system-packages .

##==============================================================================
#
.ONESHELL:
test: setup ## Run unit tests
	source "$(BIN)/activate"
	$(PYTHON) -m unittest discover -s $(TST_D) -p "test_*.py"
	coverage run --source=. -m unittest discover -s $(TST_D) -p "test_*.py"
	coverage report

##==============================================================================
#
.ONESHELL:
setup: ## Set up the project
	@$(PYTHON) -m venv $(ENV_DIR)
	@source "$(BIN)/activate"
	@pip install --upgrade pip
	@pip install .[test]

##==============================================================================
#
.ONESHELL:
update-venv: ## Update the virtual environment packages
	@source "$(BIN)/activate"
	@pip install --upgrade pip
	@pip install .

##==============================================================================
#
.ONESHELL:
run: ## Execute the program
	@make setup
	@source "$(BIN)/activate"
	@$(PYTHON) src/genskellie

##==============================================================================
#
.ONESHELL:
doc: upgrade ## Generate documentation
	#@doxygen Doxyfile
	genskellie -f -i ./docs -o ./html

##==============================================================================
#
debug: ## Enable the debugger (requires `pudb`)
	@source $(BIN)/activate  && \
	cd $(SRC_D)              && \
	python -m pudb main.py

##==============================================================================
#
clean: ## Cleanup the project
	rm -rfv $(ENV_DIR)

##==============================================================================
# https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
help:  ## Auto-generated help menu
	@grep -P '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
	sort                                                | \
	awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
