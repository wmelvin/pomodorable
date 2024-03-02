@default:
  @just --list

# Run test, lint, check, hatch build
@build: test lint check
  hatch build

# Check formatting
@check:
  hatch fmt --check

# Apply formatting
@format:
  hatch fmt

# Lint with hatch
@lint:
  hatch fmt --linter

# Run pytest
@test:
  hatch run test

# Run ui.py
@ui:
  hatch run python3 src/pomodorable/ui.py

# Run ui.py with textual --dev
@tui:
  hatch run textual run --dev src/pomodorable/ui.py

# Run 'textual colors' (color preview tool)
@tcol:
  hatch run textual colors
