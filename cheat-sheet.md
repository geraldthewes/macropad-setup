# Macropad Configuration: Emacs Workflow

Device ID: `5633`

## Macros

| Slot | Description | Actions |
|------|-------------|---------|
| 0 | ESC then W (Emacs copy) | tap(KC_ESC), tap(KC_W) |
| 1 | C-x 3 (split-window-right — vertical split) | tap(LCTL(KC_X)), delay(20), tap(KC_3) |
| 2 | C-x 2 (split-window-below — horizontal split) | tap(LCTL(KC_X)), delay(20), tap(KC_2) |
| 3 | C-x t 2 (tab-bar new tab) | tap(LCTL(KC_X)), delay(20), tap(KC_T), delay(20), tap(KC_2) |
| 4 | C-x t 0 (tab-bar close tab) | tap(LCTL(KC_X)), delay(20), tap(KC_T), delay(20), tap(KC_0) |
| 5 | C-x } (enlarge-window-horizontally) | tap(LCTL(KC_X)), delay(20), tap(LSFT(KC_RBRC)) |
| 6 | C-x { (shrink-window-horizontally) | tap(LCTL(KC_X)), delay(20), tap(LSFT(KC_LBRC)) |
| 7 | C-x ^ (enlarge-window) | tap(LCTL(KC_X)), delay(20), tap(LSFT(KC_6)) |
| 8 | C-u - C-x ^ (shrink-window) | tap(LCTL(KC_U)), delay(20), tap(KC_MINS), delay(20), tap(LCTL(KC_X)), delay(20), tap(LSFT(KC_6)) |
| 9 | C-x 0 (delete-window — close current split) | tap(LCTL(KC_X)), delay(20), tap(KC_0) |
| 10 | C-c C-e (eat: switch to emacs mode) | tap(LCTL(KC_C)), delay(20), tap(LCTL(KC_E)) |
| 11 | C-c C-j (eat: return to semi-char mode) | tap(LCTL(KC_C)), delay(20), tap(LCTL(KC_J)) |

## Layer 0: Main

### Keys

| Pos | Keycode | Description |
|-----|---------|-------------|
| 00 | `LCTL(LSFT(KC_C))` | Copy with shift (visual select + copy) |
| 01 | `LCTL(LSFT(KC_V))` | Paste (visual paste) |
| 02 | `M0` | ESC then W (Emacs copy) |
| 03 | `LCTL(KC_Y)` | Yank (redo after paste) |
| 10 | `M1` | Split vertical (C-x 3) |
| 11 | `M2` | Split horizontal (C-x 2) |
| 12 | `M3` | New tab (C-x t 2) |
| 13 | `M4` | Close tab (C-x t 0) |
| 20 | `M9` | Close split (C-x 0) |
| 21 | `LCTL(KC_Q)` | quoted-insert |
| 22 | `M10` | Eat emacs mode (C-c C-e) |
| 23 | `M11` | Eat semi-char mode (C-c C-j) |
| 30 | `LCTL(KC_C)` | Copy |
| 31 | `LCTL(KC_V)` | Paste |

### Encoders

| Encoder | Direction | Action | Description |
|---------|-----------|--------|-------------|
| Left | CW | `M5` | Horizontal resize |
| Left | CCW | `M6` | |
| Middle | CW | `M7` | Vertical resize |
| Middle | CCW | `M8` | |
| Right | CW | `KC_WH_U` | Scroll |
| Right | CCW | `KC_WH_D` | |
