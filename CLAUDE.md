# Macropad Setup

Configuration scripts for the DOIO KB16 rev2 macropad (16 keys, 3 encoder knobs).


## Hardware

- **Device**: DOIO KB16 rev2
- **Device ID**: Read from script (USB)
- **CLI tool**: `vitaly` (must be installed and the macropad must be connected via USB)

## Layout

- **Layer 0** is the only layer in use
- **Keys**: 4 columns x 4 rows (positions `row,col` from `0,0` to `3,3`)
- **Encoders**: 3 knobs — left (0), middle (1), right (2)
  - Direction 0 = counter-clockwise (CCW), direction 1 = clockwise (CW)
- **Macros**: 

## Files

- `macropad.sh` — defines all macros, key bindings, and encoder bindings
- `Makefile` — `make install` to flash settings, `make print` to display current config

## vitaly CLI reference

```bash
# Define a macro
vitaly -i 5633 macros -n <slot> -v '<macro_definition>'

# Bind a key
vitaly -i 5633 keys -l <layer> -p <row>,<col> -v '<keycode_or_macro>'

# Bind an encoder rotation
vitaly -i 5633 encoders -l <layer> -p <encoder>,<direction> -v <keycode_or_macro>

# Print current layer config
vitaly -i 5633 layers -p
```

## Keycode conventions

- Modifiers: `LCTL()`, `LSFT()`, `LALT()`, `LGUI()`
- Macro reference: `M<slot>` (e.g., `M0`, `M5`)
- Macro actions: `Tap(<keycode>)`, `Delay(<ms>)`
- Shifted symbols: `}` = `LSFT(KC_RBRC)`, `{` = `LSFT(KC_LBRC)`, `^` = `LSFT(KC_6)`
