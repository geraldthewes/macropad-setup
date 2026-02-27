#!/usr/bin/env python3
"""Unit tests for compile_macropad.py"""

from compile_macropad import (
    extract_key_info,
    generate_cheat_sheet,
    qmk_to_human,
    render_grid,
)


# ---------------------------------------------------------------------------
# qmk_to_human
# ---------------------------------------------------------------------------

class TestQmkToHuman:
    def test_simple_ctrl(self):
        assert qmk_to_human('LCTL(KC_C)') == 'C-c'

    def test_simple_alt(self):
        assert qmk_to_human('LALT(KC_W)') == 'A-w'

    def test_simple_shift(self):
        assert qmk_to_human('LSFT(KC_A)') == 'S-a'

    def test_simple_gui(self):
        assert qmk_to_human('LGUI(KC_L)') == 'G-l'

    def test_nested_ctrl_shift(self):
        assert qmk_to_human('LCTL(LSFT(KC_C))') == 'C-S-c'

    def test_nested_ctrl_alt(self):
        assert qmk_to_human('LCTL(LALT(KC_T))') == 'C-A-t'

    def test_special_spc(self):
        assert qmk_to_human('KC_SPC') == 'SPC'

    def test_special_esc(self):
        assert qmk_to_human('KC_ESC') == 'ESC'

    def test_special_tab(self):
        assert qmk_to_human('KC_TAB') == 'TAB'

    def test_bare_keycode(self):
        assert qmk_to_human('KC_X') == 'x'

    def test_bare_number(self):
        assert qmk_to_human('KC_3') == '3'

    def test_ctrl_spc(self):
        assert qmk_to_human('LCTL(KC_SPC)') == 'C-SPC'

    def test_passthrough_unknown(self):
        assert qmk_to_human('CUSTOM_KEY') == 'CUSTOM_KEY'


# ---------------------------------------------------------------------------
# extract_key_info
# ---------------------------------------------------------------------------

SAMPLE_MACROS: list[dict] = [
    {
        'id': 0,
        'description': 'CTRL-Q then ESC',
        'actions': [
            {'type': 'tap', 'keycode': 'LCTL(KC_Q)'},
            {'type': 'tap', 'keycode': 'KC_ESC'},
        ],
    },
    {
        'id': 1,
        'description': 'C-x 3',
        'actions': [
            {'type': 'tap', 'keycode': 'LCTL(KC_X)'},
            {'type': 'delay', 'ms': 20},
            {'type': 'tap', 'keycode': 'KC_3'},
        ],
    },
    {
        'id': 10,
        'description': 'C-c C-e',
        'actions': [
            {'type': 'tap', 'keycode': 'LCTL(KC_C)'},
            {'type': 'delay', 'ms': 20},
            {'type': 'tap', 'keycode': 'LCTL(KC_E)'},
        ],
    },
]


class TestExtractKeyInfo:
    def test_parens_with_key_sequence(self):
        name, seq = extract_key_info('Split vertical (C-x 3)', 'M1', SAMPLE_MACROS)
        assert name == 'Split vertical'
        assert seq == 'C-x 3'

    def test_parens_with_non_key_info(self):
        name, seq = extract_key_info('Shift-copy (visual select)', 'LCTL(LSFT(KC_C))', SAMPLE_MACROS)
        assert name == 'Shift-copy'
        assert seq == 'C-S-c'

    def test_no_parens_direct_keycode(self):
        name, seq = extract_key_info('Copy', 'LCTL(KC_C)', SAMPLE_MACROS)
        assert name == 'Copy'
        assert seq == 'C-c'

    def test_no_parens_macro_ref(self):
        # M0: CTRL-Q then ESC — no parens in description
        name, seq = extract_key_info('CTRL-Q ESC', 'M0', SAMPLE_MACROS)
        assert name == 'CTRL-Q ESC'
        # delays skipped, taps: LCTL(KC_Q) -> C-q, KC_ESC -> ESC
        assert seq == 'C-q ESC'

    def test_macro_ref_delays_skipped(self):
        # M1 has a delay between taps
        name, seq = extract_key_info('Split vertical', 'M1', SAMPLE_MACROS)
        assert name == 'Split vertical'
        assert seq == 'C-x 3'

    def test_multi_tap_macro(self):
        # M10: C-c C-e (two ctrl taps, delay in between)
        name, seq = extract_key_info('Eat emacs mode', 'M10', SAMPLE_MACROS)
        assert name == 'Eat emacs mode'
        assert seq == 'C-c C-e'

    def test_paren_with_esc(self):
        name, seq = extract_key_info('Quit (ESC)', 'KC_ESC', [])
        assert name == 'Quit'
        assert seq == 'ESC'


# ---------------------------------------------------------------------------
# render_grid
# ---------------------------------------------------------------------------

class TestRenderGrid:
    def _make_grid(self, rows: int = 4, cols: int = 4) -> list[list[tuple[str, str]]]:
        return [[('', '') for _ in range(cols)] for _ in range(rows)]

    def test_output_wrapped_in_code_fence(self):
        grid = self._make_grid()
        result = render_grid(grid)
        assert result.startswith('```\n')
        assert result.endswith('\n```')

    def test_correct_line_count(self):
        # 4 rows × 2 content lines = 8, plus top border + 3 mid borders + bottom = 5 border lines
        # Total: 8 + 5 = 13 lines inside the fence
        grid = self._make_grid()
        inner = render_grid(grid)[4:-4]  # strip ```\n and \n```
        line_count = len(inner.split('\n'))
        assert line_count == 13

    def test_empty_cells_render(self):
        grid = self._make_grid()
        result = render_grid(grid)
        assert '┌' in result
        assert '└' in result
        assert '│' in result

    def test_content_appears(self):
        grid = [[('Hello', 'C-h'), ('', '')],
                [('', ''), ('', '')]]
        result = render_grid(grid)
        assert 'Hello' in result
        assert 'C-h' in result

    def test_dynamic_column_widths(self):
        # Column 0 has a long name; column 1 has short content
        grid = [[('A very long name here', 'C-x'), ('Short', 'x')],
                [('', ''), ('', '')]]
        result = render_grid(grid)
        lines = result.split('\n')
        # The top border line reflects column widths; col 0 must be wider than col 1
        top = lines[1]  # lines[0] is ```
        # Count dashes in first and second segments
        segments = top[1:-1].split('┬')
        assert len(segments[0]) > len(segments[1])

    def test_no_markdown_table_pipes(self):
        # Should use box-drawing │ not plain | for cell separators inside content
        grid = [[('Mark', 'C-SPC'), ('Cut', 'C-w'), ('Copy', 'A-w'), ('Yank', 'C-y')],
                [('', ''), ('', ''), ('', ''), ('', '')],
                [('', ''), ('', ''), ('', ''), ('', '')],
                [('', ''), ('', ''), ('', ''), ('', '')]]
        result = render_grid(grid)
        # Should not have plain pipe characters (only box-drawing)
        assert '|' not in result


# ---------------------------------------------------------------------------
# Integration: generate_cheat_sheet
# ---------------------------------------------------------------------------

class TestGenerateCheatSheet:
    def _make_config(self) -> dict:
        return {
            'name': 'Test',
            'device_id': 5633,
            'macros': SAMPLE_MACROS,
            'layers': [
                {
                    'index': 0,
                    'name': 'Main',
                    'keys': [
                        {'row': 0, 'col': 0, 'value': 'M0', 'description': 'CTRL-Q ESC'},
                        {'row': 0, 'col': 1, 'value': 'M1', 'description': 'Split vertical (C-x 3)'},
                        {'row': 1, 'col': 0, 'value': 'LCTL(KC_SPC)', 'description': 'Mark (C-SPC)'},
                    ],
                }
            ],
        }

    def test_output_contains_box_drawing(self):
        config = self._make_config()
        result = generate_cheat_sheet(config, [], [], [])
        assert '┌' in result
        assert '└' in result

    def test_output_no_markdown_table(self):
        config = self._make_config()
        result = generate_cheat_sheet(config, [], [], [])
        # Old format used "| Pos | Role |" — should not appear
        assert '| Pos |' not in result

    def test_header_present(self):
        config = self._make_config()
        result = generate_cheat_sheet(config, [], [], [])
        assert '# Macropad Configuration: Test' in result
        assert 'Device ID: `5633`' in result

    def test_layer_header_present(self):
        config = self._make_config()
        result = generate_cheat_sheet(config, [], [], [])
        assert '## Layer 0: Main' in result

    def test_key_names_in_output(self):
        config = self._make_config()
        result = generate_cheat_sheet(config, [], [], [])
        assert 'CTRL-Q ESC' in result
        assert 'Split vertical' in result
        assert 'Mark' in result
