**✅ Complete Step-by-Step Guide: Flash DOIO KB16 rev2 from Scratch (Linux)**

This is the exact minimal path that worked reliably on Ubuntu 24.04. Total time: ~10–15 minutes once dependencies are installed.

### 1. Install system prerequisites
```bash
sudo apt update
sudo apt install -y git python3-pip python3-venv dfu-util udev
```

### 2. Install Rust (required for vitaly)
```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
source "$HOME/.cargo/env"
```

### 3. Clone official Vial-QMK firmware
```bash
git clone --recurse-submodules https://github.com/vial-kb/vial-qmk.git
cd vial-qmk
```

### 4. Run QMK setup (choose option 3)
```bash
qmk setup
```
When prompted “What do you want to do?” → type `3` and press Enter.

### 5. Install correct udev rules (critical for flashing)
```bash
sudo cp util/udev/50-qmk.rules /etc/udev/rules.d/
sudo udevadm control --reload-rules && sudo udevadm trigger
```

### 6. Create clean Vial keymap with insecure mode
```bash
# Restore the official working vial keymap
git restore keyboards/doio/kb16/rev2/keymaps/vial/keymap.c keyboards/doio/kb16/rev2/keymaps/vial/rules.mk 2>/dev/null || true

# Enable Vial + always-unlocked + encoders
cat > keyboards/doio/kb16/rev2/keymaps/vial/rules.mk << 'EOF'
VIA_ENABLE = yes
VIAL_ENABLE = yes
VIALRGB_ENABLE = yes
VIAL_INSECURE = yes
ENCODER_MAP_ENABLE = yes
EOF
```

### 7. Compile the firmware
```bash
qmk compile -kb doio/kb16/rev2 -km vial
```
You should see `Build doio/kb16/rev2:vial [OK]`

### 8. Flash the macropad (new board)
1. Unplug the macropad.  
2. Hold the **top-left key** (physical position 0,0).  
3. While holding it, plug in the USB cable → RGB turns off/solid (DFU mode).  
4. Run:
```bash
qmk flash -kb doio/kb16/rev2 -km vial
```
Success = “Download done” + “Resetting USB” (ignore final gmake Error 74 — it’s harmless).

### 9. Install vitaly CLI (pure-text config tool)
```bash
cargo install vitaly
```

### 10. Make vitaly available in every terminal (permanent)
```bash
echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### 11. Verify everything
```bash
vitaly devices          # should show id: 5633 + "vial:" serial
vitaly -i 5633 layers -p   # shows full layout
```

You now have a fully working KB16 with **4 layers**, triple-knob support, no GUI, no unlock timer, and permanent CLI config via vitaly.

**From now on you never repeat steps 1–8 again.**  
All changes = just `vitaly` commands (see the kb16-macropad-config skill for examples).

Copy this whole guide and keep it — it works on any new/fresh KB16.  

You’re done. Plug it in normally and enjoy the perfect Linux CLI macropad. 🚀
