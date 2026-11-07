import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import jaxo.tools as tools


class WorkspaceSafetyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.old = tools.WORKSPACE
        tools.WORKSPACE = Path(self.temp.name).resolve()

    def tearDown(self):
        tools.WORKSPACE = self.old
        self.temp.cleanup()

    def test_blocks_parent_traversal(self):
        with self.assertRaises(ValueError):
            tools._safe_target("../outside.txt")

    def test_blocks_absolute_path(self):
        with self.assertRaises(ValueError):
            tools._safe_target("/tmp/outside.txt")

    def test_list_empty_workspace(self):
        self.assertEqual(tools.list_files(), "(empty folder)")

    def test_creates_file_only_after_confirmation(self):
        with patch("jaxo.tools.Confirm.ask", return_value=True):
            result = tools.create_file("notes/hello.txt", "hello", None)
        self.assertIn("Saved file", result)
        self.assertEqual((tools.WORKSPACE / "notes/hello.txt").read_text(), "hello")


if __name__ == "__main__":
    unittest.main()
