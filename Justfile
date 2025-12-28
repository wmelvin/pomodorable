@default:
  @just --list

# Run test, lint, check, hatch build
@build: lint check test
  hatch build

# Check formatting
@check:
  hatch run ruff format --check

# Run lint, check, and test
@checks: lint check test

# Remove dist
@clean:
  -rm dist/*

# Apply formatting with ruff
@format: lint
  hatch run ruff format

# Run ruff check
@lint:
  hatch run ruff check

# Run pytest
@test:
  hatch run test

# Run test matrix
@testmx:
  hatch run test:test

# Run ui.py
@ui:
  hatch run python3 src/pomodorable/ui.py

# Run ui.py with textual --dev
@tui:
  hatch run textual run --dev src/pomodorable/ui.py

# Run cli.py with textual --dev
@cli:
  hatch run textual run --dev src/pomodorable/cli.py --ctrl-s --ctrl-t

# Run 'textual colors' (color preview tool)
@tcol:
  hatch run textual colors

# # Take a screenshot using textual --screenshot
# @tss:
#   hatch run textual run src/pomodorable/ui.py --screenshot 5

# Redirect help output to temp.txt
@help:
  hatch run pomodorable -h > temp.txt

# Update requirements.txt using requirements.in and pip-compile --upgrade
@pipc:
  hatch run pip-compile --upgrade requirements.in
