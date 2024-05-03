#!./venv/bin/python3

"""
A parallelized version of man_to_pdf.py.
Convert man pages for shell commands to PDF format. 

Author: Bruno Cardenas-Bourges, 2024
"""

import os
import subprocess
import sys
import time

from argparse import ArgumentParser
from concurrent.futures import ProcessPoolExecutor

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pdfdocument.document import PDFDocument


NUM_CORES = os.cpu_count()
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

# Standalone from the for loop in the original main()
def process_command(command: str) -> None:
    man_page = run_man(command)
    create_pdf(command, man_page)
    print(f"Created {command}-manual.pdf")

def main():
    parser = ArgumentParser(usage="./man_to_pdf_parallel.py [-h] command [commands ...]",
                            description="A parallelized version of man_to_pdf.py.")
    
    parser.add_argument("commands", nargs="+")
    args = parser.parse_args()

    if args.commands is None:
        parser.print_help()

    start_time = time.time()
    with ProcessPoolExecutor(max_workers=NUM_CORES) as executor:
        executor.map(process_command, args.commands)
    end_time = time.time()
    print(f"Total elapsed time: {end_time - start_time:.3f} seconds")

    print("PDF files created successfully.")


if __name__ == "__main__":
    main()
