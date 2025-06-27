# YouTube Music Downloader - Simplified Makefile
# Provides essential commands for setup, running, and managing the application

.PHONY: help install setup run check clean logs status update

# Default target
.DEFAULT_GOAL := help

# Variables
PYTHON := python3
PIP := pip3
VENV_DIR := venv
LOG_DIR := logs
DOWNLOAD_DIR := downloads

# Colors for output
GREEN := \033[0;32m
YELLOW := \033[1;33m
BLUE := \033[0;34m
RED := \033[0;31m
NC := \033[0m # No Color

help: ## Show this help message
	@echo "$(BLUE)🎵 YouTube Music Downloader - Available Commands$(NC)"
	@echo "=================================================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(GREEN)%-15s$(NC) %s\n", $$1, $$2}'

install: ## Install Python environment and dependencies
	@echo "$(BLUE)🔧 Setting up YouTube Music Downloader...$(NC)"
	@echo "$(BLUE)Creating Python virtual environment...$(NC)"
	@$(PYTHON) -m venv $(VENV_DIR)
	@echo "$(BLUE)Activating virtual environment and installing dependencies...$(NC)"
	@$(VENV_DIR)/bin/pip install --upgrade pip
	@$(VENV_DIR)/bin/pip install -r requirements.txt
	@echo "$(BLUE)Creating directories...$(NC)"
	@mkdir -p $(LOG_DIR) $(DOWNLOAD_DIR)
	@echo "$(GREEN)✅ Installation complete!$(NC)"
	@echo "$(YELLOW)Run 'make run' to start the downloader$(NC)"

setup: ## Setup directories and check dependencies
	@echo "$(BLUE)Setting up directories...$(NC)"
	@mkdir -p $(LOG_DIR) $(DOWNLOAD_DIR)
	@echo "$(GREEN)✅ Setup complete$(NC)"

run: ## Run the YouTube downloader
	@echo "$(BLUE)🎵 Starting YouTube Music Downloader...$(NC)"
	@if [ -d "$(VENV_DIR)" ]; then \
		$(VENV_DIR)/bin/python downloader.py; \
	else \
		$(PYTHON) downloader.py; \
	fi

check: ## Check system requirements and dependencies
	@echo "$(BLUE)🔍 Checking system requirements...$(NC)"
	@if [ -d "$(VENV_DIR)" ]; then \
		$(VENV_DIR)/bin/python check_system.py; \
	else \
		$(PYTHON) check_system.py; \
	fi

clean: ## Clean up temporary files and cache
	@echo "$(BLUE)🧹 Cleaning up...$(NC)"
	@rm -rf __pycache__/
	@rm -rf .pytest_cache/
	@rm -rf *.pyc
	@find . -name "*.tmp" -delete 2>/dev/null || true
	@find . -name "*.part" -delete 2>/dev/null || true
	@echo "$(GREEN)✅ Cleanup complete$(NC)"

clean-all: ## Remove everything including virtual environment
	@echo "$(YELLOW)⚠️  This will remove the virtual environment and all temporary files$(NC)"
	@read -p "Are you sure? (y/N): " confirm && [ "$$confirm" = "y" ] || exit 1
	@$(MAKE) clean
	@rm -rf $(VENV_DIR)
	@echo "$(GREEN)✅ Complete cleanup done$(NC)"

logs: ## Show recent log entries
	@echo "$(BLUE)📋 Recent log entries:$(NC)"
	@if [ -d $(LOG_DIR) ] && [ -n "$$(ls -A $(LOG_DIR) 2>/dev/null)" ]; then \
		tail -n 30 $(LOG_DIR)/*.log 2>/dev/null | head -50; \
	else \
		echo "$(YELLOW)⚠️  No log files found$(NC)"; \
	fi

status: ## Show application status and statistics
	@echo "$(BLUE)📊 Application Status:$(NC)"
	@echo "===================="
	@echo "Python: $$($(PYTHON) --version 2>/dev/null || echo 'Not found')"
	@echo "Virtual Environment: $$([ -d $(VENV_DIR) ] && echo 'Active' || echo 'Not found')"
	@echo "yt-dlp: $$(yt-dlp --version 2>/dev/null || echo 'Not installed')"
	@echo "Download directory: $(DOWNLOAD_DIR)"
	@echo "Log directory: $(LOG_DIR)"
	@if [ -d $(DOWNLOAD_DIR) ]; then \
		echo "Downloaded files: $$(find $(DOWNLOAD_DIR) -type f 2>/dev/null | wc -l)"; \
		echo "Storage used: $$(du -sh $(DOWNLOAD_DIR) 2>/dev/null | cut -f1)"; \
	fi
	@if [ -d $(LOG_DIR) ]; then \
		echo "Log files: $$(find $(LOG_DIR) -name '*.log' 2>/dev/null | wc -l)"; \
	fi

update: ## Update yt-dlp to latest version
	@echo "$(BLUE)📦 Updating yt-dlp...$(NC)"
	@if [ -d "$(VENV_DIR)" ]; then \
		$(VENV_DIR)/bin/pip install --upgrade yt-dlp; \
	else \
		$(PIP) install --upgrade yt-dlp; \
	fi
	@echo "$(GREEN)✅ yt-dlp updated$(NC)"

deps: ## Show installed dependencies
	@echo "$(BLUE)📦 Installed dependencies:$(NC)"
	@if [ -d "$(VENV_DIR)" ]; then \
		$(VENV_DIR)/bin/pip list | grep -E "(yt-dlp|rich)"; \
	else \
		$(PIP) list | grep -E "(yt-dlp|rich)"; \
	fi

dev-install: ## Install development dependencies
	@echo "$(BLUE)📦 Installing development dependencies...$(NC)"
	@if [ -d "$(VENV_DIR)" ]; then \
		$(VENV_DIR)/bin/pip install ruff pytest; \
	else \
		$(PIP) install ruff pytest; \
	fi
	@echo "$(GREEN)✅ Development dependencies installed$(NC)"

test: ## Run basic functionality test
	@echo "$(BLUE)🧪 Running basic test...$(NC)"
	@if [ -d "$(VENV_DIR)" ]; then \
		$(VENV_DIR)/bin/python -c "import yt_dlp; print('✅ yt-dlp import successful')"; \
		$(VENV_DIR)/bin/python -c "from rich.console import Console; Console().print('[green]✅ Rich import successful[/green]')"; \
	else \
		$(PYTHON) -c "import yt_dlp; print('✅ yt-dlp import successful')"; \
		$(PYTHON) -c "from rich.console import Console; Console().print('[green]✅ Rich import successful[/green]')"; \
	fi

# Quick aliases
i: install ## Alias for install
r: run ## Alias for run
s: status ## Alias for status
c: check ## Alias for check
u: update ## Alias for update

# Help text for unknown targets
%:
	@echo "$(RED)❌ Unknown target: $@$(NC)"
	@echo "$(BLUE)Run 'make help' to see available commands$(NC)"
