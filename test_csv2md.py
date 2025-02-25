#!/usr/bin/env -S uv run --script
"""Tests for csv2md module."""

import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout, redirect_stderr
from io import StringIO

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import csv2md


class TestCSVToMarkdownTable(unittest.TestCase):
    """Test cases for csv2md.py."""

    def test_csv_to_md_table_basic(self) -> None:
        """Tests basic CSV to Markdown table conversion."""
        csv_content = "Name,Age,City\nJohn,30,New York\nJane,25,Los Angeles"
        expected = "| Name | Age | City |\n| --- | --- | --- |\n| John | 30 | New York |\n| Jane | 25 | Los Angeles |"
        result = csv2md.csv_to_md_table(csv_content)
        self.assertEqual(result, expected)

    def test_csv_to_md_table_empty(self) -> None:
        """Tests conversion with empty CSV."""
        csv_content = ""
        expected = "Empty CSV data."
        result = csv2md.csv_to_md_table(csv_content)
        self.assertEqual(result, expected)

    def test_csv_to_md_table_header_only(self) -> None:
        """Tests conversion with header only."""
        csv_content = "Name,Age,City"
        expected = "| Name | Age | City |\n| --- | --- | --- |"
        result = csv2md.csv_to_md_table(csv_content)
        self.assertEqual(result, expected)

    def test_csv_to_md_table_uneven_columns(self) -> None:
        """Tests handling of rows with varying column counts."""
        csv_content = "Name,Age,City\nJohn,30\nJane,25,Los Angeles,USA"
        expected = "| Name | Age | City |\n| --- | --- | --- |\n| John | 30 |  |\n| Jane | 25 | Los Angeles |"
        result = csv2md.csv_to_md_table(csv_content)
        self.assertEqual(result, expected)

    def test_csv_to_md_table_custom_delimiter(self) -> None:
        """Tests conversion with custom delimiter."""
        csv_content = "Name;Age;City\nJohn;30;New York\nJane;25;Los Angeles"
        expected = "| Name | Age | City |\n| --- | --- | --- |\n| John | 30 | New York |\n| Jane | 25 | Los Angeles |"
        result = csv2md.csv_to_md_table(csv_content, delimiter=";")
        self.assertEqual(result, expected)

    def test_read_csv_file_from_string(self) -> None:
        """Tests reading CSV content from file path."""
        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp:
            tmp.write("Name,Age,City\nJohn,30,New York")
            tmp_path = tmp.name

        try:
            content = csv2md.read_csv_file(tmp_path)
            self.assertEqual(content, "Name,Age,City\nJohn,30,New York")
        finally:
            os.unlink(tmp_path)

    def test_read_csv_file_from_file_object(self) -> None:
        """Tests reading CSV content from file object."""
        file_obj = StringIO("Name,Age,City\nJohn,30,New York")
        content = csv2md.read_csv_file(file_obj)
        self.assertEqual(content, "Name,Age,City\nJohn,30,New York")

    def test_main_function_file_to_stdout(self) -> None:
        """Tests main function with file input to stdout."""
        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp:
            tmp.write("Name,Age,City\nJohn,30,New York")
            tmp_path = tmp.name

        try:
            # Redirect stdout to capture output
            stdout_capture = StringIO()
            with redirect_stdout(stdout_capture):
                sys.argv = ["csv2md.py", tmp_path]
                csv2md.main()

            output = stdout_capture.getvalue().strip()
            expected = (
                "| Name | Age | City |\n| --- | --- | --- |\n| John | 30 | New York |"
            )
            self.assertEqual(output, expected)
        finally:
            os.unlink(tmp_path)

    def test_main_function_file_to_file(self) -> None:
        """Tests main function with file input to file output."""
        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as input_tmp:
            input_tmp.write("Name,Age,City\nJohn,30,New York")
            input_path = input_tmp.name

        output_path = tempfile.mktemp()

        try:
            sys.argv = ["csv2md.py", input_path, "-o", output_path]
            csv2md.main()

            with open(output_path, "r") as f:
                output = f.read().strip()

            expected = (
                "| Name | Age | City |\n| --- | --- | --- |\n| John | 30 | New York |"
            )
            self.assertEqual(output, expected)
        finally:
            if os.path.exists(input_path):
                os.unlink(input_path)
            if os.path.exists(output_path):
                os.unlink(output_path)

    def test_error_handling(self) -> None:
        """Tests error handling for non-existent file."""
        stderr_capture = StringIO()
        with redirect_stderr(stderr_capture), self.assertRaises(SystemExit):
            sys.argv = ["csv2md.py", "non_existent_file.csv"]
            csv2md.main()

        error_output = stderr_capture.getvalue()
        self.assertIn("Error", error_output)


if __name__ == "__main__":
    unittest.main()
