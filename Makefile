MAKEFLAGS += --no-print-directory

# Do not remove this block. It is used by the 'help' rule when
# constructing the help output.
# help:
# help: Redis arXiv Search App Makefile help
# help:

SHELL:=/bin/bash
CONDA_ACTIVATE=source $$(conda info --base)/etc/profile.d/conda.sh ; conda activate ; conda activate

# help: help                      - display this makefile's help information
.PHONY: help
help:
	@grep "^# help\:" Makefile | grep -v grep | sed 's/\# help\: //' | sed 's/\# help\://'

# help:
# help: Conda Environment Setup
# help: -------------

# help: env                   - setup a Python conda env for this application
.PHONY: env
env:
	@conda create -n arXiv python=3.9 -y
	$(CONDA_ACTIVATE) arXiv
	@backend/ \
	&& python -m pip install -r requirements.txt \
	&& python -m pip install -r frontend_streamlit/requirements.txt

# help:
# help: Run streamlit app
# help: -------------

# help: run_app                      - runs the streamlit app
.PHONY: run_app
run_app:
	@PYTHONPATH=. streamlit run frontend_streamlit/streamlit_app.py

# help: run_qa_example                      - runs the question answering example
.PHONY: run_qa_example
run_qa_example:
	@PYTHONPATH=. python redis_player_one/haystack/example.py


# help:
# help: Run linter
# help: -------------

# help: run_linter                      - lint code
.PHONY: run_linter
run_linter:
	@echo "Running linter"
	@isort .
	@flake8 .

# help:
# help: Install requirements
# help: -------------

# help: install_requirements                      - install requirements
.PHONY: install_requirements
install_requirements:
	@echo "Initialization: Installing pip-tools and requirements"
	@python -m pip install pip-tools==6.6.2
	@pip-compile requirements.in
	@python -m pip install -r requirements.txt