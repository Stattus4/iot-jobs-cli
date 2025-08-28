PROJECT_DIR := $(shell pwd)
DOCKER_COMPOSE := docker/docker-compose.yml
LOCAL_DIR := $(PROJECT_DIR)/openapi-generator-cli/local
REQUIREMENTS := $(PROJECT_DIR)/requirements.txt 
VENV_DIR := $(PROJECT_DIR)/.venv

UID := $(shell id -u)
GID := $(shell id -g)

.PHONY: all
all: run-openapi-generator-cli install-openapi-generator-cli

.PHONY: venv
venv:
	@if [ ! -d "$(VENV_DIR)" ]; then \
		echo ">>> Creating Python virtual environment..."; \
		python3 -m venv $(VENV_DIR); \
	fi

.PHONY: check-local-dir
check-local-dir:
	@if [ ! -d "$(LOCAL_DIR)" ]; then \
		echo ">>> Creating $(LOCAL_DIR) directory..."; \
		mkdir -p $(LOCAL_DIR); \
	fi
	@if [ "$$(stat -c '%u:%g' $(LOCAL_DIR))" != "$(UID):$(GID)" ]; then \
		echo ">>> Fixing $(LOCAL_DIR) directory ownership..."; \
		chown -R $(UID):$(GID) $(LOCAL_DIR); \
	fi

.PHONY: run-openapi-generator-cli
run-openapi-generator-cli: check-local-dir
	@echo ">>> Running OpenAPI Generator CLI..."
	LOCAL_UID=$(UID) LOCAL_GID=$(GID) docker compose -f $(DOCKER_COMPOSE) run --rm openapi-generator-cli

.PHONY: install-openapi-generator-cli
install-openapi-generator-cli: venv
	@echo ">>> Installing OpenAPI Generator CLI..."
	. $(VENV_DIR)/bin/activate && \
		pip install --upgrade pip && \
		pip install -e $(LOCAL_DIR)/ && \
		pip install -r $(REQUIREMENTS)

.PHONY: uninstall-openapi-generator-cli
uninstall-openapi-generator-cli:
	@echo ">>> Checking for installed OpenAPI Generator CLI..."
	. $(VENV_DIR)/bin/activate && \
		if pip show openapi_client > /dev/null 2>&1; then \
			echo ">>> Uninstalling OpenAPI Generator CLI..." && \
			pip uninstall -y openapi_client; \
		else \
			echo ">>> OpenAPI Generator CLI not installed, skipping uninstall."; \
		fi

.PHONY: clean
clean: uninstall-openapi-generator-cli
	@echo ">>> Cleaning OpenAPI Generator CLI files..."
	find $(LOCAL_DIR) -mindepth 1 ! -name '.gitkeep' -exec rm -rf {} +
