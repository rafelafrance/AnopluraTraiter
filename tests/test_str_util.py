"""Tests for the str_util module."""

import unittest

from anoplura.pylib.str_util import strip_json_fences


class TestStripJsonFences(unittest.TestCase):
    """Tests for strip_json_fences."""

    def test_json_tag(self) -> None:
        """Strip fences with a json language tag."""
        input_text = '```json\n{"key": "value"}\n```'
        self.assertEqual(strip_json_fences(input_text), '{"key": "value"}')

    def test_python_tag(self) -> None:
        """Strip fences with a python language tag."""
        input_text = '```python\n{"key": "value"}\n```'
        self.assertEqual(strip_json_fences(input_text), '{"key": "value"}')

    def test_text_tag(self) -> None:
        """Strip fences with a text language tag."""
        input_text = '```text\n{"key": "value"}\n```'
        self.assertEqual(strip_json_fences(input_text), '{"key": "value"}')

    def test_no_tag(self) -> None:
        """Strip fences without any language tag."""
        input_text = '```\n{"key": "value"}\n```'
        self.assertEqual(strip_json_fences(input_text), '{"key": "value"}')

    def test_no_fence(self) -> None:
        """Return bare JSON unchanged."""
        input_text = '{"key": "value"}'
        self.assertEqual(strip_json_fences(input_text), '{"key": "value"}')

    def test_extra_whitespace_around(self) -> None:
        """Handle leading and trailing whitespace outside fences."""
        input_text = '  ```json\n{"key": "value"}\n```  '
        self.assertEqual(strip_json_fences(input_text), '{"key": "value"}')

    def test_four_backticks(self) -> None:
        """Strip fences with four backticks."""
        input_text = '````json\n{"key": "value"}\n````'
        self.assertEqual(strip_json_fences(input_text), '{"key": "value"}')

    def test_five_backticks(self) -> None:
        """Strip fences with five backticks."""
        input_text = '`````json\n{"key": "value"}\n`````'
        self.assertEqual(strip_json_fences(input_text), '{"key": "value"}')

    def test_empty_input(self) -> None:
        """Return empty string for empty input."""
        self.assertEqual(strip_json_fences(""), "")

    def test_missing_closing_fence(self) -> None:
        """Return input unchanged when closing fence is missing."""
        input_text = '```json\n{"key": "value"}'
        self.assertEqual(strip_json_fences(input_text), '```json\n{"key": "value"}')

    def test_missing_opening_fence(self) -> None:
        """Return input unchanged when opening fence is missing."""
        input_text = '{"key": "value"}\n```'
        self.assertEqual(strip_json_fences(input_text), '{"key": "value"}\n```')

    def test_multiline_json(self) -> None:
        """Strip fences around multi-line JSON content."""
        input_text = '```json\n{\n  "key": "value",\n  "nested": {\n    "a": 1\n}\n```'
        expected = '{\n  "key": "value",\n  "nested": {\n    "a": 1\n}'
        self.assertEqual(strip_json_fences(input_text), expected)

    def test_nested_fences(self) -> None:
        """Handle backticks appearing within the JSON content."""
        input_text = '```json\n{\n  "code": "```\n"}\n```'
        expected = '{\n  "code": "```\n"}'
        self.assertEqual(strip_json_fences(input_text), expected)

    def test_only_opening_fence(self) -> None:
        """Return input unchanged when only an opening fence exists."""
        input_text = "```json"
        self.assertEqual(strip_json_fences(input_text), "```json")

    def test_only_closing_fence(self) -> None:
        """Return input unchanged when only a closing fence exists."""
        input_text = "```"
        self.assertEqual(strip_json_fences(input_text), "```")

    def test_whitespace_only_fence(self) -> None:
        """Return empty string when fences enclose only whitespace."""
        input_text = "```json\n\n```"
        self.assertEqual(strip_json_fences(input_text), "")


if __name__ == "__main__":
    unittest.main()
