@default:
  @just --list

# Check formatting
@check:
  hatch fmt --check

# Fix formatting
@fix:
  hatch fmt

# Run pytest
@test:
  hatch run test

# Run ui.py
@ui:
  hatch run python3 src/pomodorable/ui.py

# Run ui.py with textual --dev
@tui:
  hatch run textual run --dev src/pomodorable/ui.py
