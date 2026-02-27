#!/usr/bin/env python3
"""
Compiler for macropad YAML configuration.
Reads a declarative YAML config and generates:
- macropad.sh: vitaly commands to configure the device
- cheat-sheet.md: human-readable documentation
"""

import argparse
from pathlib import Path
from typing import Any

import yaml


def load_yaml(path: Path) -> dict[str, Any]:
    """Load and parse YAML configuration file."""
    with open(path) as f:
        return yaml.safe_load(f)


def validate_config(config: dict[str, Any]) -> None:
    """Validate the YAML configuration schema."""
    required = ['device_id', 'layers']
    for field in required:
        if field not in config:
            raise ValueError(f"Missing required field: {field}")

    if not isinstance(config['layers'], list):
        raise ValueError("'layers' must be a list")

    for layer in config['layers']:
        if 'index' not in layer:
            raise ValueError("Each layer must have an 'index' field")


def parse_macro_action(action: str | dict) -> str:
    """Convert YAML macro action to vitaly syntax."""
    if isinstance(action, str):
        # Direct keycode like "KC_ESC"
        return f"Tap({action})"

    if not isinstance(action, dict):
        raise ValueError(f"Invalid macro action: {action}")

    action_type = action.get('type')
    if action_type == 'tap':
        return f"Tap({action['keycode']})"
    elif action_type == 'delay':
        return f"Delay({action['ms']})"
    elif action_type == 'down':
        return f"Down({action['keycode']})"
    elif action_type == 'up':
        return f"Up({action['keycode']})"
    else:
        raise ValueError(f"Unknown macro action type: {action_type}")


def compile_macro(macro: dict[str, Any], slot: int) -> str:
    """Compile a macro definition to vitaly syntax."""
    actions = macro.get('actions', [])
    if not actions:
        raise ValueError(f"Macro {slot} has no actions")

    parts = [parse_macro_action(a) for a in actions]
    return '; '.join(parts)


def generate_macros(config: dict[str, Any]) -> list[tuple[int, str, str]]:
    """Generate macro definitions. Returns list of (slot, vitaly_command, description)."""
    macros = []
    device_id = config['device_id']
    defined_macros = config.get('macros', [])
    used_ids = set()

    # First pass: process macros with explicit IDs
    for macro in defined_macros:
        if 'id' in macro:
            slot = macro['id']
            if slot in used_ids:
                raise ValueError(f"Duplicate macro slot: {slot}")
            used_ids.add(slot)
            vitaly_cmd = f"vitaly -i {device_id} macros -n {slot} -v '{compile_macro(macro, slot)}'"
            macros.append((slot, vitaly_cmd, macro.get('description', '')))

    # Second pass: assign IDs to macros without explicit IDs
    next_id = 0
    for macro in defined_macros:
        if 'id' not in macro:
            while next_id in used_ids:
                next_id += 1
            slot = next_id
            used_ids.add(slot)
            vitaly_cmd = f"vitaly -i {device_id} macros -n {slot} -v '{compile_macro(macro, slot)}'"
            macros.append((slot, vitaly_cmd, macro.get('description', '')))
            next_id += 1

    return sorted(macros, key=lambda x: x[0])


def generate_keys(config: dict[str, Any]) -> list[tuple[str, str, str]]:
    """Generate key bindings. Returns list of (position, vitaly_command, description)."""
    keys = []
    device_id = config['device_id']

    for layer in config['layers']:
        layer_idx = layer['index']
        for key in layer.get('keys', []):
            row = key['row']
            col = key['col']
            position = f"{row},{col}"
            value = key['value']
            description = key.get('description', '')

            vitaly_cmd = f"vitaly -i {device_id} keys -l {layer_idx} -p {position} -v '{value}'"
            keys.append((position, vitaly_cmd, description))

    return sorted(keys, key=lambda x: x[0])


def generate_encoders(config: dict[str, Any]) -> list[tuple[str, str, str]]:
    """Generate encoder bindings. Returns list of (position, vitaly_command, description)."""
    encoders = []
    device_id = config['device_id']

    for layer in config['layers']:
        layer_idx = layer['index']
        for encoder in layer.get('encoders', []):
            encoder_idx = encoder['encoder']
            for direction in ['cw', 'ccw']:
                if direction in encoder:
                    dir_idx = 1 if direction == 'cw' else 0
                    position = f"{encoder_idx},{dir_idx}"
                    value = encoder[direction]
                    description = encoder.get('description', '')

                    dir_name = 'CW' if direction == 'cw' else 'CCW'
                    vitaly_cmd = f"vitaly -i {device_id} encoders -l {layer_idx} -p {position} -v {value}"
                    encoders.append((position, vitaly_cmd, f"{description} ({dir_name})" if description else dir_name))

    return sorted(encoders, key=lambda x: x[0])


def resolve_macro_reference(value: str, macros: list) -> str:
    """If value is like 'M0', return the macro description; otherwise return value as-is."""
    if value.startswith('M') and value[1:].isdigit():
        slot = int(value[1:])
        for s, _, desc in macros:
            if s == slot:
                return desc
    return value


def qmk_to_human(value: str) -> str:
    """Translate a QMK keycode expression to human-readable Emacs-style notation."""
    value = value.strip()

    # Check for modifier wrappers
    modifier_map = {
        'LCTL': 'C-',
        'LSFT': 'S-',
        'LALT': 'A-',
        'LGUI': 'G-',
    }
    for mod, prefix in modifier_map.items():
        if value.startswith(f'{mod}(') and value.endswith(')'):
            inner = value[len(mod) + 1:-1]
            return prefix + qmk_to_human(inner)

    # Strip KC_ prefix
    if value.startswith('KC_'):
        key = value[3:]
        special = {'SPC': 'SPC', 'ESC': 'ESC', 'TAB': 'TAB'}
        if key in special:
            return special[key]
        return key.lower()

    return value


def _is_key_sequence(text: str) -> bool:
    """Return True if text looks like a key sequence (e.g. C-x 3, ESC, A-w)."""
    import re
    modifier_pattern = re.compile(r'\b[CASG]-')
    known_special = {'ESC', 'SPC', 'TAB', 'RET'}
    if modifier_pattern.search(text):
        return True
    for word in text.split():
        if word in known_special:
            return True
    return False


def extract_key_info(
    description: str,
    value: str,
    config_macros: list[dict[str, Any]],
) -> tuple[str, str]:
    """Return (display_name, key_sequence) for a key binding.

    Rules:
    1. Parens with key sequence  → name before parens, sequence from inside parens
    2. Parens with non-key info  → name before parens, sequence via qmk_to_human
    3. No parens, direct keycode → name = description, sequence via qmk_to_human
    4. No parens, macro ref      → name = description, sequence from macro actions
    """
    import re

    paren_match = re.search(r'\(([^)]+)\)$', description.strip())
    if paren_match:
        paren_content = paren_match.group(1)
        name = description[: paren_match.start()].strip()
        if _is_key_sequence(paren_content):
            return name, paren_content
        else:
            return name, qmk_to_human(value)

    # No parens
    name = description

    # Macro reference like M0, M10
    if re.match(r'^M\d+$', value):
        slot = int(value[1:])
        macro = next((m for m in config_macros if m.get('id') == slot), None)
        if macro:
            taps = []
            for action in macro.get('actions', []):
                if isinstance(action, dict) and action.get('type') == 'delay':
                    continue
                if isinstance(action, dict) and action.get('type') in ('tap', 'down', 'up'):
                    taps.append(qmk_to_human(action['keycode']))
                elif isinstance(action, str):
                    taps.append(qmk_to_human(action))
            return name, ' '.join(taps)
        return name, value

    return name, qmk_to_human(value)


def render_grid(grid: list[list[tuple[str, str]]]) -> str:
    """Render a 4x4 grid of (name, sequence) tuples as a Unicode box-drawing table."""
    rows = len(grid)
    cols = max(len(row) for row in grid) if grid else 0

    # Compute column widths: max content width per column (+ 2 for padding)
    col_widths = []
    for c in range(cols):
        width = 0
        for r in range(rows):
            if c < len(grid[r]):
                name, seq = grid[r][c]
                width = max(width, len(name), len(seq))
        col_widths.append(width + 2)  # 1 space padding each side

    def hline(left: str, mid: str, right: str, fill: str) -> str:
        parts = [fill * w for w in col_widths]
        return left + mid.join(parts) + right

    lines: list[str] = []
    lines.append(hline('┌', '┬', '┐', '─'))

    for r, row in enumerate(grid):
        # Line 1: name
        cells_name = []
        cells_seq = []
        for c in range(cols):
            w = col_widths[c]
            if c < len(row):
                name, seq = row[c]
            else:
                name, seq = '', ''
            cells_name.append(f' {name:<{w - 1}}')
            cells_seq.append(f' {seq:<{w - 1}}')

        lines.append('│' + '│'.join(cells_name) + '│')
        lines.append('│' + '│'.join(cells_seq) + '│')

        if r < rows - 1:
            lines.append(hline('├', '┼', '┤', '─'))

    lines.append(hline('└', '┴', '┘', '─'))

    return '```\n' + '\n'.join(lines) + '\n```'


def generate_cheat_sheet(config: dict[str, Any], macros: list, keys: list, encoders: list) -> str:
    """Generate human-readable cheat sheet markdown."""
    config_macros: list[dict[str, Any]] = config.get('macros', [])

    lines: list[str] = []
    lines.append(f"# Macropad Configuration: {config.get('name', 'Unnamed')}")
    lines.append("")
    lines.append(f"Device ID: `{config['device_id']}`")
    lines.append("")

    for layer in config['layers']:
        lines.append(f"## Layer {layer['index']}: {layer.get('name', 'Unnamed')}")
        lines.append("")
        lines.append("### Keys")
        lines.append("")

        # Build 4x4 grid
        layer_key_map: dict[str, dict[str, Any]] = {}
        for key in layer.get('keys', []):
            layer_key_map[f"{key['row']},{key['col']}"] = key

        grid: list[list[tuple[str, str]]] = []
        for row in range(4):
            grid_row: list[tuple[str, str]] = []
            for col in range(4):
                key = layer_key_map.get(f"{row},{col}")
                if key:
                    name, seq = extract_key_info(
                        key.get('description', ''),
                        key['value'],
                        config_macros,
                    )
                    grid_row.append((name, seq))
                else:
                    grid_row.append(('', ''))
            grid.append(grid_row)

        lines.append(render_grid(grid))

        # Encoders for this layer
        if layer.get('encoders'):
            lines.append("")
            lines.append("### Encoders")
            lines.append("")
            lines.append("| Encoder | Direction | Action | Description |")
            lines.append("|---------|-----------|--------|-------------|")

            for encoder in layer['encoders']:
                enc_idx = encoder['encoder']
                enc_name = ['Left', 'Middle', 'Right'][enc_idx] if enc_idx < 3 else f"Encoder {enc_idx}"

                if 'cw' in encoder or 'ccw' in encoder:
                    cw_action = encoder.get('cw', 'N/A')
                    ccw_action = encoder.get('ccw', 'N/A')
                    desc = encoder.get('description', '')
                    lines.append(f"| {enc_name} | CW | {resolve_macro_reference(cw_action, macros)} | {desc} |")
                    lines.append(f"| {enc_name} | CCW | {resolve_macro_reference(ccw_action, macros)} | |")

        lines.append("")

    return "\n".join(lines)


def generate_shell_script(macros: list, keys: list, encoders: list, comments: dict) -> str:
    """Generate the bash script with vitaly commands."""
    lines = []
    lines.append("#!/bin/bash")
    lines.append("")

    # Macros
    for slot, cmd, description in macros:
        if description:
            lines.append(f"# Macro {slot}: {description}")
        lines.append(cmd)
        lines.append("")

    # Keys grouped by row
    current_row = None
    for position, cmd, description in keys:
        row = int(position.split(',')[0])
        if current_row is not None and row != current_row:
            lines.append("")
        current_row = row

        if description:
            lines.append(f"# {description}")
        lines.append(cmd)

    lines.append("")

    # Encoders grouped by encoder
    current_encoder = None
    for position, cmd, description in encoders:
        encoder = int(position.split(',')[0])

        if current_encoder is not None and encoder != current_encoder:
            lines.append("")
        current_encoder = encoder

        lines.append(f"# {description}")
        lines.append(cmd)

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Compile macropad YAML config to shell script")
    parser.add_argument('config_file', type=Path, help="Path to YAML config file")
    parser.add_argument('--output-sh', type=Path, default=Path('macropad.sh'),
                        help="Output shell script path")
    parser.add_argument('--output-md', type=Path, default=Path('cheat-sheet.md'),
                        help="Output cheat sheet path")
    args = parser.parse_args()

    config = load_yaml(args.config_file)
    validate_config(config)

    # Generate all bindings
    macros = generate_macros(config)
    keys = generate_keys(config)
    encoders = generate_encoders(config)

    # Generate output files
    shell_script = generate_shell_script(macros, keys, encoders, {})
    cheat_sheet = generate_cheat_sheet(config, macros, keys, encoders)

    # Write outputs
    with open(args.output_sh, 'w') as f:
        f.write(shell_script)
    print(f"Generated: {args.output_sh}")

    with open(args.output_md, 'w') as f:
        f.write(cheat_sheet)
    print(f"Generated: {args.output_md}")


if __name__ == '__main__':
    main()
