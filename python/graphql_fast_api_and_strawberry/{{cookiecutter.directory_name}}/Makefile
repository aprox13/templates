PYTHON_MAJOR={{cookiecutter.pythonMajor}}
PYTHON_MINOR={{cookiecutter.pythonMinor}}

PYTHON_VERSION=${PYTHON_MAJOR}.${PYTHON_MINOR}
PIP=pip${PYTHON_VERSION}
PYTHON=python${PYTHON_VERSION}
VENV_FOLDER="venv"

PYTHON_BINARY=${VENV_FOLDER}/bin/${PYTHON}

init/venv:
	@./scripts/init.sh init_venv $(shell pwd) ${PYTHON_VERSION} ${VENV_FOLDER}

install:
	@${PYTHON_BINARY} -m pip install --upgrade pip
	@${PYTHON_BINARY} -m pip install --no-cache-dir --upgrade -r requirements.txt

init: init/venv install

info:
	@echo "Python:" $(shell ${PYTHON_BINARY} -V)
	@echo "Pip:" "$(shell ${PYTHON_BINARY} -m pip -V)"
	@echo "Dependencies:"
	@${PYTHON_BINARY} -m pip freeze

format:
	@${VENV_FOLDER}/bin/black -t "py${PYTHON_MAJOR}${PYTHON_MINOR}" .
