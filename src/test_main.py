from unittest import TestCase
from main import extract_title


class TestMain(TestCase):
    def test_extract_title(self):
        self.assertEqual("Header 1", extract_title("# Header 1"))

        with self.assertRaises(ValueError):
            extract_title("#Header 1")

        with self.assertRaises(ValueError):
            extract_title("Test Markdown")

        self.assertEqual("Header line 2", extract_title(
            "Test Markdown\n# Header line 2"))
