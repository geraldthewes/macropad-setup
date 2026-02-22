# Macropad Configuration: Emacs Workflow

Device ID: `5633`

## Layer 0: Main

### Keys

| Pos | Role | Description |
|-----|---------|-------------|
| 00 | LCTL(LSFT(KC_C)) | Copy with shift (visual select + copy) |
| 01 | LCTL(LSFT(KC_V)) | Paste (visual paste) |
| 02 | ESC then W (Emacs copy) | ESC then W (Emacs copy) |
| 03 | LCTL(KC_Y) | Yank (redo after paste) |
| 10 | C-x 3 (split-window-right — vertical split) | Split vertical (C-x 3) |
| 11 | C-x 2 (split-window-below — horizontal split) | Split horizontal (C-x 2) |
| 12 | C-x t 2 (tab-bar new tab) | New tab (C-x t 2) |
| 13 | C-x t 0 (tab-bar close tab) | Close tab (C-x t 0) |
| 20 | C-x 0 (delete-window — close current split) | Close split (C-x 0) |
| 21 | LCTL(KC_Q) | quoted-insert |
| 22 | C-c C-e (eat: switch to emacs mode) | Eat emacs mode (C-c C-e) |
| 23 | C-c C-j (eat: return to semi-char mode) | Eat semi-char mode (C-c C-j) |
| 30 | LCTL(KC_C) | Copy |
| 31 | LCTL(KC_V) | Paste |

### Encoders

| Encoder | Direction | Action | Description |
|---------|-----------|--------|-------------|
| Left | CW | C-x } (enlarge-window-horizontally) | Horizontal resize |
| Left | CCW | C-x { (shrink-window-horizontally) | |
| Middle | CW | C-x ^ (enlarge-window) | Vertical resize |
| Middle | CCW | C-u - C-x ^ (shrink-window) | |
| Right | CW | KC_WH_U | Scroll |
| Right | CCW | KC_WH_D | |
