# Macropad YAML DSL

A declarative YAML-based configuration format for the DOIO KB16 macropad.

## Overview

This DSL allows you to define your macropad configuration in a human-readable YAML file. The compiler generates:
- `macropad.sh` - Executable bash script to program the hardware via Vitaly CLI
- `cheat-sheet.md` - Human-readable documentation with key descriptions

## Quick Start

1. Create a configuration file (see `examples/` for templates)
2. Run the compiler:

```bash
python compile_macropad.py your-config.yaml
```

3. Flash to your macropad:

```bash
./macropad.sh
```

Or simply use `make install` if you have a Makefile set up.

## Configuration File Format

```yaml
version: 1.0
device:
  id: 5633
  name: DOIO KB16 Megalodon

layers:
  - number: 0
    name: Base (Emacs)
    keys:
      - pos: [0, 0]
        keycode: LCTL(LSFT(KC_C))
        desc: "Copy (Ctrl+Shift+C)"
    encoders:
      - id: 0
        cw: macro_id: 5
        ccw: macro_id: 6
        desc_cw: "Zoom in"
        desc_ccw: "Zoom out"

macros:
  - id: 0
    name: emacs_copy
    actions: [Tap(KC_ESC), Tap(KC_W)]
    desc: "Emacs copy command"
```

## Key Features

- **Human-readable**: YAML with clear descriptions for every key
- **Self-documenting**: Generates a cheat sheet from your config
- **Version-controlled**: Git-friendly configuration format
- **Validated**: Schema validation catches errors before flashing

## Documentation

- [Specification](./specification.md) - Complete DSL schema reference
- [PRD](./prd.md) - Product requirements and design rationale

## Requirements

- Python 3.10+
- [Vitaly CLI](https://github.com/bskaplou/vitaly) installed
- DOIO KB16 (rev2) macropad with Vial firmware
