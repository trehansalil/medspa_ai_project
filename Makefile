PROJECT_NAME:="medspa-ai"
BIN_LINUX := venv/bin
BIN_WINDOWS := venv/Scripts/python

ifeq ($(OS),Windows_NT)
    BIN := $(BIN_WINDOWS)
    COVERAGE_CMD := $(BIN) -m coverage
else
    BIN := $(BIN_LINUX)
    COVERAGE_CMD := $(BIN)/coverage
endif


run:
ifeq ($(OS),Windows_NT)
	echo "Windows detected"
	$(BIN) app.py
else
	echo "Linux/MacOS detected"
	$(BIN)/python3 app.py
endif

setup:
ifeq ($(OS),Windows_NT)
	echo "Windows detected"
	@$(BIN) -m pip install poetry
	@$(BIN) -m poetry install --sync
else
	echo "Linux/MacOS detected"
	@$(BIN)/pip install poetry
	@$(BIN)/poetry install --sync
endif

update_dependencies:
ifeq ($(OS),Windows_NT)
	echo "Windows detected"
	@$(BIN) -m poetry export -f requirements.txt --without-hashes --output requirements.txt
else
	echo "Linux/MacOS detected"
	@$(BIN)/poetry export -f requirements.txt --without-hashes --output requirements.txt
endif
