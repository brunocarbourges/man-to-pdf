#!./venv/bin/python3

"""
Convert man pages for shell commands to PDF format. 
You may pass one or more shell commands as arguments. Will overwrite existing files with names of the form <command>-manual.pdf.

Author: Bruno Cardenas-Bourges, 2024
"""

import subprocess
import sys
import time

from argparse import ArgumentParser

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pdfdocument.document import PDFDocument


FONT = TTFont("Menlo", "./fonts/Menlo-Regular.ttf")
pdfmetrics.registerFont(FONT)


def run_man(command: str) -> str:
    try:
        # col -b removes backspace control sequences in 'man' output
        result = subprocess.run(f"man {command} | col -b", shell=True, text=True, capture_output=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        sys.exit(1)

def create_pdf(command: str, content: str) -> None:
    file_name = f"{command}-manual.pdf"
    pdf = PDFDocument(file_name)
    pdf.font_name = "Menlo"
    pdf.init_report()
    pdf.p(content)
    pdf.generate()

def main():
    parser = ArgumentParser(usage="./man_to_pdf.py [-h] command [commands ...]",
                            description="Convert man pages for shell commands to PDF format.")
    
    parser.add_argument("commands", nargs="+")
    args = parser.parse_args()

    if args.commands is None:
        parser.print_help()

    for command in args.commands:
        start_time = time.time()
        man_page = run_man(command)
        create_pdf(command, man_page)
        end_time = time.time()
        print(f"Created {command}-manual.pdf in {end_time - start_time:.3f} seconds")

    print("PDF files created successfully.")


if __name__ == "__main__":
    main()
