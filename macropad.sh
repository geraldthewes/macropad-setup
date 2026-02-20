#!/bin/bash

# Macro 0: ESC then W (Emacs copy)
vitaly -i 5633 macros -n 0 -v 'Tap(KC_ESC); Tap(KC_W)'

# Macro 1: C-x 3 (split-window-right — vertical split)
vitaly -i 5633 macros -n 1 -v 'Tap(LCTL(KC_X)); Delay(20); Tap(KC_3)'

# Macro 2: C-x 2 (split-window-below — horizontal split)
vitaly -i 5633 macros -n 2 -v 'Tap(LCTL(KC_X)); Delay(20); Tap(KC_2)'

# Macro 3: C-x t 2 (tab-bar new tab)
vitaly -i 5633 macros -n 3 -v 'Tap(LCTL(KC_X)); Delay(20); Tap(KC_T); Delay(20); Tap(KC_2)'

# Macro 4: C-x t 0 (tab-bar close tab)
vitaly -i 5633 macros -n 4 -v 'Tap(LCTL(KC_X)); Delay(20); Tap(KC_T); Delay(20); Tap(KC_0)'

# Macro 5: C-x } (enlarge-window-horizontally)
vitaly -i 5633 macros -n 5 -v 'Tap(LCTL(KC_X)); Delay(20); Tap(LSFT(KC_RBRC))'

# Macro 6: C-x { (shrink-window-horizontally)
vitaly -i 5633 macros -n 6 -v 'Tap(LCTL(KC_X)); Delay(20); Tap(LSFT(KC_LBRC))'

# Macro 7: C-x ^ (enlarge-window)
vitaly -i 5633 macros -n 7 -v 'Tap(LCTL(KC_X)); Delay(20); Tap(LSFT(KC_6))'

# Macro 8: C-u - C-x ^ (shrink-window)
vitaly -i 5633 macros -n 8 -v 'Tap(LCTL(KC_U)); Delay(20); Tap(KC_MINS); Delay(20); Tap(LCTL(KC_X)); Delay(20); Tap(LSFT(KC_6))'

# Macro 9: C-x 0 (delete-window — close current split)
vitaly -i 5633 macros -n 9 -v 'Tap(LCTL(KC_X)); Delay(20); Tap(KC_0)'

# Macro 10: C-c C-e (eat: switch to emacs mode)
vitaly -i 5633 macros -n 10 -v 'Tap(LCTL(KC_C)); Delay(20); Tap(LCTL(KC_E))'

# Macro 11: C-c C-j (eat: return to semi-char mode)
vitaly -i 5633 macros -n 11 -v 'Tap(LCTL(KC_C)); Delay(20); Tap(LCTL(KC_J))'

# Copy with shift (visual select + copy)
vitaly -i 5633 keys -l 0 -p 0,0 -v 'LCTL(LSFT(KC_C))'
# Paste (visual paste)
vitaly -i 5633 keys -l 0 -p 0,1 -v 'LCTL(LSFT(KC_V))'
# ESC then W (Emacs copy)
vitaly -i 5633 keys -l 0 -p 0,2 -v 'M0'
# Yank (redo after paste)
vitaly -i 5633 keys -l 0 -p 0,3 -v 'LCTL(KC_Y)'

# Split vertical (C-x 3)
vitaly -i 5633 keys -l 0 -p 1,0 -v 'M1'
# Split horizontal (C-x 2)
vitaly -i 5633 keys -l 0 -p 1,1 -v 'M2'
# New tab (C-x t 2)
vitaly -i 5633 keys -l 0 -p 1,2 -v 'M3'
# Close tab (C-x t 0)
vitaly -i 5633 keys -l 0 -p 1,3 -v 'M4'

# Close split (C-x 0)
vitaly -i 5633 keys -l 0 -p 2,0 -v 'M9'
# quoted-insert
vitaly -i 5633 keys -l 0 -p 2,1 -v 'LCTL(KC_Q)'
# Eat emacs mode (C-c C-e)
vitaly -i 5633 keys -l 0 -p 2,2 -v 'M10'
# Eat semi-char mode (C-c C-j)
vitaly -i 5633 keys -l 0 -p 2,3 -v 'M11'

# Copy
vitaly -i 5633 keys -l 0 -p 3,0 -v 'LCTL(KC_C)'
# Paste
vitaly -i 5633 keys -l 0 -p 3,1 -v 'LCTL(KC_V)'

# Horizontal resize (CCW)
vitaly -i 5633 encoders -l 0 -p 0,0 -v M6
# Horizontal resize (CW)
vitaly -i 5633 encoders -l 0 -p 0,1 -v M5

# Vertical resize (CCW)
vitaly -i 5633 encoders -l 0 -p 1,0 -v M8
# Vertical resize (CW)
vitaly -i 5633 encoders -l 0 -p 1,1 -v M7

# Scroll (CCW)
vitaly -i 5633 encoders -l 0 -p 2,0 -v KC_WH_D
# Scroll (CW)
vitaly -i 5633 encoders -l 0 -p 2,1 -v KC_WH_U