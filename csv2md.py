#!/usr/bin/env -S uv run --script
"""Module for converting CSV data to Markdown tables.

This module provides functions to read CSV files or strings and convert them
to Markdown formatted tables.
"""

import argparse
import csv
import io
import sys
from typing import IO, Union


def read_csv_file(file_path_or_obj: Union[str, IO]) -> str:
    """Reads content from a CSV file or file object.

    Args:
        file_path_or_obj: CSV file path (str) or file object

    Returns:
        A string containing the CSV content.

    Raises:
        IOError: An error occurred reading the CSV file.
    """
    try:
        if isinstance(file_path_or_obj, str):
            with open(file_path_or_obj, "r", encoding="utf-8") as f:
                return f.read()
        else:
            return file_path_or_obj.read()
    except Exception as e:
        raise IOError(f"Error occurred while reading CSV file: {e}")


def csv_to_md_table(csv_content: str, delimiter: str = ",") -> str:
    """Converts CSV string to Markdown table format.

    Args:
        csv_content: CSV formatted string
        delimiter: CSV delimiter character

    Returns:
        A string containing the Markdown formatted table.
    """
    try:
        # Process string as CSV
        reader = csv.reader(io.StringIO(csv_content), delimiter=delimiter)
        rows = list(reader)

        if not rows:
            return "Empty CSV data."

        # Store header row for reuse
        header_row = rows[0]

        # Create header and separator rows
        header = "| " + " | ".join(header_row) + " |"
        separator = "| " + " | ".join(["---"] * len(header_row)) + " |"

        data_rows = []
        for row in rows[1:]:
            # Fill with empty strings if row is shorter than header
            if len(row) < len(header_row):
                row.extend([""] * (len(header_row) - len(row)))
            # Truncate row if it's longer than header
            elif len(row) > len(header_row):
                row = row[: len(header_row)]
            data_rows.append("| " + " | ".join(row) + " |")

        md_table = "\n".join([header, separator] + data_rows)

        return md_table

    except Exception as e:
        return f"An error occurred: {e}"


def main() -> None:
    """Main entry point for the CSV to Markdown table converter."""
    parser = argparse.ArgumentParser(
        description="Convert CSV files to Markdown tables."
    )
    parser.add_argument(
        "input", nargs="?", help="Input CSV file (uses stdin if omitted)"
    )
    parser.add_argument(
        "-o", "--output", help="Output file (displays to stdout if omitted)"
    )
    parser.add_argument(
        "-d",
        "--delimiter",
        default=",",
        help="CSV delimiter character (default: comma)",
    )

    args = parser.parse_args()

    try:
        # Determine input source and read content
        if args.input:
            csv_content = read_csv_file(args.input)
        else:
            csv_content = read_csv_file(sys.stdin)

        # Convert CSV to Markdown table
        md_table = csv_to_md_table(csv_content, delimiter=args.delimiter)

        # Determine output destination
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(md_table)
        else:
            print(md_table)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
