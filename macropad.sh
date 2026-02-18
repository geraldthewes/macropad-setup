#!/bin/bash
# 1. Define macro slot 0 = ESC then W (Emacs copy)
vitaly -i 5633 macros -n 0 -v 'Tap(KC_ESC); Tap(KC_W)'

# 2. Set the 4 keys
vitaly -i 5633 keys -l 0 -p 0,0 -v 'LCTL(LSFT(KC_C))'
vitaly -i 5633 keys -l 0 -p 0,1 -v 'LCTL(LSFT(KC_V))'
vitaly -i 5633 keys -l 0 -p 0,2 -v "M0"
vitaly -i 5633 keys -l 0 -p 0,3 -v 'LCTL(KC_Y)'

# ── Row 1: Emacs window/tab management ──

# Macro 1: C-x 3 (split-window-right — vertical split)
vitaly -i 5633 macros -n 1 -v 'Tap(LCTL(KC_X)); Delay(20); Tap(KC_3)'

# Macro 2: C-x 2 (split-window-below — horizontal split)
vitaly -i 5633 macros -n 2 -v 'Tap(LCTL(KC_X)); Delay(20); Tap(KC_2)'

# Macro 3: C-x t 2 (tab-bar new tab)
vitaly -i 5633 macros -n 3 -v 'Tap(LCTL(KC_X)); Delay(20); Tap(KC_T); Delay(20); Tap(KC_2)'

# Macro 4: C-x t 0 (tab-bar close tab)
vitaly -i 5633 macros -n 4 -v 'Tap(LCTL(KC_X)); Delay(20); Tap(KC_T); Delay(20); Tap(KC_0)'

# Bind row 1 keys
vitaly -i 5633 keys -l 0 -p 1,0 -v 'M1'
vitaly -i 5633 keys -l 0 -p 1,1 -v 'M2'
vitaly -i 5633 keys -l 0 -p 1,2 -v 'M3'
vitaly -i 5633 keys -l 0 -p 1,3 -v 'M4'
