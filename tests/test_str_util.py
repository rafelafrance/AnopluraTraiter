import unittest

from anoplura.pylib.str_util import strip_json_fences


class TestStripJsonFences(unittest.TestCase):
    def test_json_tag(self):
        input_text = '```json\n{"key": "value"}\n```'
        self.assertEqual(strip_json_fences(input_text), '{"key": "value"}')

    def test_python_tag(self):
        input_text = '```python\n{"key": "value"}\n```'
        self.assertEqual(strip_json_fences(input_text), '{"key": "value"}')

    def test_text_tag(self):
        input_text = '```text\n{"key": "value"}\n```'
        self.assertEqual(strip_json_fences(input_text), '{"key": "value"}')

    def test_no_tag(self):
        input_text = '```\n{"key": "value"}\n```'
        self.assertEqual(strip_json_fences(input_text), '{"key": "value"}')

    def test_no_fence(self):
        input_text = '{"key": "value"}'
        self.assertEqual(strip_json_fences(input_text), '{"key": "value"}')

    def test_extra_whitespace_around(self):
        input_text = '  ```json\n{"key": "value"}\n```  '
        self.assertEqual(strip_json_fences(input_text), '{"key": "value"}')

    def test_four_backticks(self):
        input_text = '````json\n{"key": "value"}\n````'
        self.assertEqual(strip_json_fences(input_text), '{"key": "value"}')

    def test_five_backticks(self):
        input_text = '`````json\n{"key": "value"}\n`````'
        self.assertEqual(strip_json_fences(input_text), '{"key": "value"}')

    def test_empty_input(self):
        self.assertEqual(strip_json_fences(""), "")

    def test_missing_closing_fence(self):
        input_text = '```json\n{"key": "value"}'
        self.assertEqual(strip_json_fences(input_text), '```json\n{"key": "value"}')

    def test_missing_opening_fence(self):
        input_text = '{"key": "value"}\n```'
        self.assertEqual(strip_json_fences(input_text), '{"key": "value"}\n```')

    def test_multiline_json(self):
        input_text = '```json\n{\n  "key": "value",\n  "nested": {\n    "a": 1\n}\n```'
        expected = '{\n  "key": "value",\n  "nested": {\n    "a": 1\n}'
        self.assertEqual(strip_json_fences(input_text), expected)

    def test_nested_fences(self):
        input_text = '```json\n{\n  "code": "```\n"}\n```'
        expected = '{\n  "code": "```\n"}'
        self.assertEqual(strip_json_fences(input_text), expected)

    def test_only_opening_fence(self):
        input_text = "```json"
        self.assertEqual(strip_json_fences(input_text), "```json")

    def test_only_closing_fence(self):
        input_text = "```"
        self.assertEqual(strip_json_fences(input_text), "```")

    def test_whitespace_only_fence(self):
        input_text = "```json\n\n```"
        self.assertEqual(strip_json_fences(input_text), "")


if __name__ == "__main__":
    unittest.main()
