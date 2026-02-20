**Key Points**  
- No dedicated DSL exists specifically for Vitaly/Vial macropad configuration, but YAML-based keymap formats are the established standard in the keyboard community (used by ZMK firmware, keymap-drawer for QMK/Vial visualization, and Vial-to-keymap converters).  
- The proposed DSL is a clean, human-readable YAML file (`macropad-config.yaml`) where every key includes its QMK/Vitaly keycode **and** a plain-English description (perfect for your Emacs bindings).  
- A single Python “compiler” script turns the YAML into: (1) a ready-to-run `macropad.sh` that calls `vitaly` to program the hardware, and (2) a beautifully formatted `cheat-sheet.md` with tables, layer overviews, and optional layout images.  
- The solution works with your existing DOIO KB16 (rev2) + Vial firmware + Vitaly CLI setup; no firmware changes required.  

**DSL Example (macropad-config.yaml)**  
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

**How the Compiler Works**  
1. Read and validate the YAML.  
2. Generate macros (if any) via `vitaly macros -n X -v '...'`.  
3. Generate key/encoder assignments via `vitaly keys …` and `vitaly encoders …`.  
4. Output `macropad.sh` (executable bash with all commands).  
5. Output `cheat-sheet.md` (Markdown tables + optional rendered layout image).  

Run with `python compile_macropad.py macropad-config.yaml` → instant programming + documentation.  

**Next Steps for the Coding Agent**  
Implement the Python compiler (using PyYAML + subprocess for Vitaly calls). Start with the current `macropad.sh` bindings as the reference example. Full PRD details below.  

---

The macropad-setup repository provides a complete, production-ready workflow for the DOIO KB16 (Megalodon) 16-key + triple-knob macropad using Vial firmware and the Vitaly CLI tool. The INSTALL.md file details flashing the custom Vial firmware (with VIAL_INSECURE and ENCODER_MAP_ENABLE), installing Vitaly via Cargo or Homebrew, and verifying the device ID (5633). The macropad.sh script is a self-contained bash file that issues dozens of Vitaly commands to define 12 Emacs-centric macros and bind them to specific physical positions on layer 0, plus encoder rotations for window resizing and scrolling. The Makefile offers simple targets (`make install` runs the script; `make print` dumps the live layer). CLAUDE.md supplies quick-reference Vitaly syntax and QMK keycode conventions (modifiers, macro references like M0, Tap/Delay, shifted symbols).  

This setup is already excellent for Emacs users, but every change currently requires hand-editing the bash script and manually tracking what each key “means.” The requested DSL eliminates that friction.  

### Research Summary on Existing DSLs and Tools in the Space  
No off-the-shelf DSL exists that directly targets Vitaly or DOIO macropads and produces both a programming script **and** a human-readable cheat sheet. However, the keyboard community has converged on YAML as the de-facto human-editable format:  
- ZMK firmware uses YAML for entire keymaps (layers, behaviors, encoders).  
- keymap-drawer (and its Vial-to-keymap-drawer converter) consumes a standardized YAML representation of QMK/Vial layouts to generate SVG/PNG visuals.  
- Tools like qmk-json or custom Python generators translate declarative configs into C keymap files or flashing scripts.  

These precedents make YAML the obvious choice: it is already familiar to anyone who has edited a ZMK config or keymap-drawer file, supports comments, hierarchical structure (layers → keys → descriptions), and is trivial to parse in Python.  

### Proposed Product Requirements (PRD)  

**1. Functional Requirements**  
- **Input**: Single `macropad-config.yaml` file. Must be git-friendly, versioned, and editable in any text editor with full comments.  
- **Core Entities Supported** (must cover everything in current macropad.sh and future expansion):  
  - Multiple layers (number + optional name).  
  - Per-key: position (row, col), keycode (raw QMK string or alias), optional macro definition, required human description.  
  - Encoders: per-encoder ID, CW/CCW actions (keycode or macro reference), descriptions.  
  - Macros: named list with sequence of Tap(), Delay(), Down(), Up() actions (Vitaly syntax).  
  - Optional: combos, tap-dances, RGB presets, QMK settings (future-proof).  
- **Output 1 – Programming Script** (`macropad.sh`):  
  - Shebang + set -e.  
  - All macro definitions first.  
  - All key and encoder bindings.  
  - Comments mirroring the YAML descriptions.  
  - Device ID taken from YAML (default 5633).  
- **Output 2 – Cheat Sheet** (`cheat-sheet.md`):  
  - Title, hardware photo, layer selector.  
  - One Markdown table per layer (columns: Physical Position, Keycode, Human Description, Visual Icon if applicable).  
  - Encoder summary section.  
  - “How to flash” reminder from INSTALL.md.  
  - Optional embedded layout image (generated via keymap-drawer or static photo).  

**2. Non-Functional Requirements**  
- Language: Python 3.10+ (PyYAML, argparse, subprocess; no external deps beyond standard library where possible).  
- Validation: Schema check (positions within 4×4 grid for KB16, valid QMK keycodes via simple regex or lookup).  
- Idempotent: running the generated script multiple times is safe.  
- Extensible: easy to add new features (e.g., layer switching keys, RGB).  
- Documentation: generated cheat sheet must be printable and readable on a phone.  
- Performance: < 2 seconds to compile even with 4 layers and 50 macros.  

**3. Detailed YAML Schema (v1.0)**  
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

Key object example:  
```yaml
- pos: [1, 0]          # row 1, column 0
  keycode: "MACRO(1)"  # or raw QMK string
  macro:               # inline macro if desired
    id: 1
    actions: [...]
  desc: "Emacs split window vertically (C-x 3)"
```

**4. Compiler Architecture**  
- `compile_macropad.py <config.yaml> [--output-dir .]`  
- Steps (in code comments for the agent):  
  1. Load & validate YAML.  
  2. Collect all macros → assign sequential IDs if not specified.  
  3. Generate bash header + macro commands.  
  4. Generate key/encoder commands using exact Vitaly syntax from CLAUDE.md and macropad.sh.  
  5. Write macropad.sh (chmod +x).  
  6. Generate Markdown tables (use Python Markdown or simple string templates).  
  7. Optionally call keymap-drawer (if installed) or embed a static image.  

**5. Migration of Current macropad.sh**  
The compiler must reproduce every binding exactly when fed a YAML that mirrors the existing macros and positions. A reference YAML for the current Emacs setup will be provided in the repo as `examples/current-emacs.yaml`.  

**6. Example Outputs**  
- `macropad.sh` will be identical in function to the existing one, but generated and commented with the human descriptions.  
- `cheat-sheet.md` will contain a clean table:

| Layer | Position | Binding                  | Meaning                              |
|-------|----------|--------------------------|--------------------------------------|
| 0     | (1,0)    | Macro 1 (C-x 3)          | Split window vertically (Emacs)      |

**7. Testing & Acceptance Criteria**  
- Run compiler on example YAML → compare generated macropad.sh with gold-standard version (diff ignoring comments).  
- Flash to real hardware (or use `vitaly devices` in CI simulation).  
- Cheat sheet renders correctly on GitHub and prints nicely.  
- Edge cases: empty layers, complex macros with Delay(100), multiple encoders, layer 1–3.  

**8. Future Enhancements (Nice-to-Haves)**  
- Emacs-specific shorthand parser: `emacs: C-x 3` → auto-generates Tap sequence and description.  
- Visual layout preview using keymap-drawer integration.  
- Support for other DOIO models (KB04, KB30, etc.) via device matrix definition.  
- GitHub Action that recompiles on config push and commits the outputs.  

This PRD, combined with the existing macropad-setup repo, INSTALL.md, macropad.sh, and Vitaly documentation, gives a coding agent everything needed to deliver a production-quality DSL in a single focused sprint. The result will make your Emacs macropad fully declarative, self-documenting, and maintainable for years.  

No open questions—implementation can start immediately.  

**Key Citations**  
- https://github.com/geraldthewes/macropad-setup (INSTALL.md, macropad.sh, CLAUDE.md, Makefile)  
- https://github.com/bskaplou/vitaly (Vitaly CLI documentation and usage examples)  
- https://github.com/YAL-Tools/vial-to-keymap-drawer and https://github.com/caksoylar/keymap-drawer (YAML keymap standards)  
- https://get.vial.today/manual/ (Vial features and keycode reference)  
- https://raw.githubusercontent.com/geraldthewes/macropad-setup/main/macropad.sh (exact current bindings)  
- https://github.com/vial-kb/vial-qmk (firmware context for DOIO KB16)
