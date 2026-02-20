# YAML DSL Specification v1.0

This document describes the formal YAML schema for the macropad configuration DSL.

## Schema

```yaml
version: 1.0
device:
  id: 5633
  model: DOIO KB16 rev2
  rows: 4
  cols: 4

layers:
  - number: 0
    name: Base (Emacs)
    keys: [...]          # list of key objects
    encoders: [...]      # list of encoder objects

macros:
  - id: 0
    name: emacs_copy
    actions: [Tap(KC_ESC), Tap(KC_W)]
    desc: "Emacs copy command"
```

## Key Object

Each key in the configuration is defined as:

```yaml
- pos: [1, 0]          # row 1, column 0
  keycode: "MACRO(1)"  # or raw QMK string
  macro:               # inline macro if desired
    id: 1
    actions: [...]
  desc: "Emacs split window vertically (C-x 3)"
```

## Encoder Object

```yaml
- id: 0  # left knob (0=left, 1=middle, 2=right)
  cw: macro_id: 5
  ccw: macro_id: 6
  desc_cw: "Enlarge window horizontally (C-x })"
  desc_ccw: "Shrink window horizontally (C-x {)"
```

## Full Example

```yaml
version: 1.0
device:
  id: 5633
  name: DOIO KB16 Megalodon

layers:
  - number: 0
    name: Base (Emacs)
    keys:
      - pos: [0, 0]   # row, col
        keycode: LCTL(LSFT(KC_C))
        desc: "Copy (Ctrl+Shift+C)"
      - pos: [0, 2]
        macro:
          id: 0
          actions: [Tap(KC_ESC), Tap(KC_W)]
        desc: "Emacs copy (ESC W)"
      - pos: [1, 0]
        macro:
          id: 1
          actions: [Tap(KC_C), Tap(KC_X), Tap(KC_3)]
        desc: "Emacs split window vertically (C-x 3)"
    encoders:
      - id: 0  # left knob
        cw: macro_id: 5
        ccw: macro_id: 6
        desc_cw: "Enlarge window horizontally (C-x })"
        desc_ccw: "Shrink window horizontally (C-x {)"
```

## Field Reference

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `version` | string | Yes | DSL version (currently "1.0") |
| `device.id` | integer | Yes | USB device ID (5633 for DOIO KB16) |
| `device.model` | string | No | Device model name |
| `device.rows` | integer | No | Number of rows (4 for KB16) |
| `device.cols` | integer | No | Number of columns (4 for KB16) |
| `layers` | array | Yes | List of layer definitions |
| `layers[].number` | integer | Yes | Layer number (0-3) |
| `layers[].name` | string | No | Human-readable layer name |
| `layers[].keys` | array | Yes | List of key bindings |
| `layers[].encoders` | array | No | List of encoder bindings |
| `keys[].pos` | array | Yes | `[row, col]` position (0-indexed) |
| `keys[].keycode` | string | No* | QMK keycode string |
| `keys[].macro` | object | No* | Inline macro definition |
| `keys[].desc` | string | Yes | Human description |
| `encoders[].id` | integer | Yes | Encoder ID (0=left, 1=middle, 2=right) |
| `encoders[].cw` | string | Yes | Clockwise action |
| `encoders[].ccw` | string | Yes | Counter-clockwise action |
| `encoders[].desc_cw` | string | No | CW description |
| `encoders[].desc_ccw` | string | No | CCW description |
| `macros` | array | No | List of macro definitions |
| `macros[].id` | integer | Yes | Macro slot number |
| `macros[].name` | string | No | Macro name |
| `macros[].actions` | array | Yes | List of actions (Tap, Delay, Down, Up) |
| `macros[].desc` | string | No | Macro description |

* Either `keycode` or `macro` must be specified for each key.

## Action Types

- `Tap(keycode)` - Press and release a key
- `Delay(ms)` - Wait for specified milliseconds
- `Down(keycode)` - Press and hold a key
- `Up(keycode)` - Release a key
