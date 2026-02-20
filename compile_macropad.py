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


def format_position(row: int, col: int) -> str:
    """Format key position for display."""
    labels = ['0', '1', '2', '3']
    return f"{labels[row]}{labels[col]}"


def generate_cheat_sheet(config: dict[str, Any], macros: list, keys: list, encoders: list) -> str:
    """Generate human-readable cheat sheet markdown."""
    lines = []
    lines.append(f"# Macropad Configuration: {config.get('name', 'Unnamed')}")
    lines.append("")
    lines.append(f"Device ID: `{config['device_id']}`")
    lines.append("")

    # Macros section
    lines.append("## Macros")
    lines.append("")
    lines.append("| Slot | Description | Actions |")
    lines.append("|------|-------------|---------|")

    for slot, _, description in macros:
        macro = None
        for m in config.get('macros', []):
            if m.get('id') == slot or (slot == 0 and not m.get('id')):
                macro = m
                break

        if macro:
            actions_str = ", ".join(str(a) if isinstance(a, str) else f"{a.get('type')}({a.get('keycode') or a.get('ms')})"
                                    for a in macro.get('actions', []))
        else:
            actions_str = ""

        lines.append(f"| {slot} | {description} | {actions_str} |")

    lines.append("")

    # Keys section per layer
    for layer in config['layers']:
        lines.append(f"## Layer {layer['index']}: {layer.get('name', 'Unnamed')}")
        lines.append("")
        lines.append("### Keys")
        lines.append("")
        lines.append("| Pos | Keycode | Description |")
        lines.append("|-----|---------|-------------|")

        layer_keys = [k for k in keys]
        for row in range(4):
            for col in range(4):
                position = f"{row},{col}"
                key_data = None
                for pos, _, desc in layer_keys:
                    if pos == position:
                        key_data = (pos, desc)
                        break

                if key_data:
                    key = next((k for k in layer.get('keys', []) if k['row'] == row and k['col'] == col), None)
                    if key:
                        lines.append(f"| {format_position(row, col)} | `{key['value']}` | {key.get('description', '')} |")

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
                    lines.append(f"| {enc_name} | CW | `{cw_action}` | {desc} |")
                    lines.append(f"| {enc_name} | CCW | `{ccw_action}` | |")

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
