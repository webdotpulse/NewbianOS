# ==============================================================================
# NewbianOS Build, Test & Distribution Makefile
# ==============================================================================

SHELL := /bin/bash
ROOT_DIR := $(shell pwd)

.PHONY: all help test lint iso test-vm clean local-install

all: help

help:
	@echo "======================================================================"
	@echo "⚡ NewbianOS 13 (Nexus) Build & Development System"
	@echo "======================================================================"
	@echo "  make test          Run unit & integration test suites"
	@echo "  make lint          Validate scripts, package lists & desktop entries"
	@echo "  make iso           Build bootable live ISO image (requires sudo)"
	@echo "  make test-vm       Launch latest ISO in QEMU/KVM virtual machine"
	@echo "  make local-install Install packages into local user environment"
	@echo "  make clean         Clean build artifacts and caches"
	@echo "======================================================================"

test:
	@echo "🧪 Running NewbianOS Test Suite..."
	python3 -m unittest discover -s tests -v

lint:
	@echo "🔍 Linting shell scripts and chroot hooks..."
	@bash -n scripts/build-iso.sh
	@bash -n scripts/test-vm.sh
	@bash -n packages/antigravity-integration/bin/antigravity-ide
	@bash -n packages/antigravity-integration/bin/agy
	@bash -n packages/antigravity-integration/bin/newbian-rollback
	@bash -n packages/antigravity-integration/bin/agy-swarm
	@bash -n packages/antigravity-integration/bin/newbian-stream
	@bash -n packages/antigravity-integration/bin/agy-box
	@bash -n packages/antigravity-integration/bin/newbian-tpm-enclave
	@bash -n packages/jarvis-assistant/bin/jarvisd
	@bash -n packages/jarvis-assistant/bin/jarvis
	@bash -n packages/jarvis-assistant/bin/jarvis-hud
	@bash -n packages/google-chrome-integration/bin/google-chrome-newbian
	@bash -n packages/google-drive-sync/bin/gdrive
	@bash -n packages/figma-integration/bin/figma-desktop
	@bash -n installer/interactive-installer/bin/newbian-installer
	@find iso-builder/config/hooks -name "*.hook.chroot" -exec bash -n {} +
	@echo "✓ All scripts and hooks syntax verified!"

iso:
	@echo "🚀 Initiating NewbianOS ISO Generation Pipeline..."
	sudo ./scripts/build-iso.sh

test-vm:
	@echo "🖥️  Starting QEMU Virtual Machine..."
	./scripts/test-vm.sh

local-install:
	@echo "📦 Linking NewbianOS utilities to ~/.local/bin..."
	mkdir -p $(HOME)/.local/bin
	ln -sf $(ROOT_DIR)/packages/antigravity-integration/bin/antigravity-ide $(HOME)/.local/bin/
	ln -sf $(ROOT_DIR)/packages/antigravity-integration/bin/agy $(HOME)/.local/bin/
	ln -sf $(ROOT_DIR)/packages/antigravity-integration/bin/newbian-rollback $(HOME)/.local/bin/
	ln -sf $(ROOT_DIR)/packages/antigravity-integration/bin/agy-swarm $(HOME)/.local/bin/
	ln -sf $(ROOT_DIR)/packages/antigravity-integration/bin/newbian-stream $(HOME)/.local/bin/
	ln -sf $(ROOT_DIR)/packages/antigravity-integration/bin/agy-box $(HOME)/.local/bin/
	ln -sf $(ROOT_DIR)/packages/antigravity-integration/bin/newbian-tpm-enclave $(HOME)/.local/bin/
	ln -sf $(ROOT_DIR)/packages/jarvis-assistant/bin/jarvis $(HOME)/.local/bin/
	ln -sf $(ROOT_DIR)/packages/jarvis-assistant/bin/jarvisd $(HOME)/.local/bin/
	ln -sf $(ROOT_DIR)/packages/jarvis-assistant/bin/jarvis-hud $(HOME)/.local/bin/
	ln -sf $(ROOT_DIR)/packages/google-chrome-integration/bin/google-chrome-newbian $(HOME)/.local/bin/
	ln -sf $(ROOT_DIR)/packages/google-drive-sync/bin/gdrive $(HOME)/.local/bin/
	ln -sf $(ROOT_DIR)/packages/figma-integration/bin/figma-desktop $(HOME)/.local/bin/
	ln -sf $(ROOT_DIR)/packages/figma-integration/bin/figma-font-helper $(HOME)/.local/bin/
	ln -sf $(ROOT_DIR)/installer/interactive-installer/bin/newbian-installer $(HOME)/.local/bin/
	@echo "✓ Linked all utilities to ~/.local/bin."

clean:
	@echo "🧹 Cleaning build artifacts..."
	rm -rf build/
	rm -rf packages/jarvis-assistant/jarvis/__pycache__
	rm -rf packages/google-drive-sync/gdrive/__pycache__
	@echo "✓ Workspace clean."
