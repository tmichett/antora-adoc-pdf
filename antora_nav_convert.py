#!/usr/bin/python3

import re
import os
import sys

# Ensure a file is provided as an argument
if len(sys.argv) < 2:
    print("Usage: python script.py <input_file>")
    sys.exit(1)

# Get the input file from command line
input_file = sys.argv[1]

# Validate input file existence
if not os.path.isfile(input_file):
    print(f"Error: File '{input_file}' not found.")
    sys.exit(1)

# Generate output filename by appending '-book' before the extension
base_name, ext = os.path.splitext(input_file)
output_file = f"{base_name}-book{ext}"

# Base directory for pages (assumed structure)
pages_dir = "pages"
os.makedirs(pages_dir, exist_ok=True)

# Read book structure snippet
book_structure_file = "book_structure_snippet.adoc"
book_structure_content = ""
if os.path.isfile(book_structure_file):
    with open(book_structure_file, "r") as bs_file:
        book_structure_content = bs_file.read() + "\n\n"

# Read the original file
with open(input_file, "r") as file:
    content = file.read()

# Regex to match xrefs like `xref:module-01.adoc#bfxactivity[Break-Fix Activity]`
xref_pattern = r"\*\*\s*xref:(module-\d{2}\.adoc)(#[^\[]*)?\[(.*?)\]"

# Extract unique modules and prepare include statements
modules = set(re.findall(r"xref:(module-\d{2}\.adoc)", content))

# Write the refined AsciiDoc file
with open(output_file, "w") as refined:
    refined.write(book_structure_content)
    refined.write("= Documentation Book\n")
    refined.write("Author Name\n")
    refined.write("v1.0\n")
    refined.write(":sectnums:\n:toc:\n:pdf-page-size: A4\n\n")

    for module in sorted(modules):
        # Ensure unique module files exist in `pages/`
        module_path = os.path.join(pages_dir, module)
        if not os.path.exists(module_path):
            with open(module_path, "w") as mod_file:
                mod_file.write(f"= {module.replace('.adoc', '').title()}\n\n")
                mod_file.write("== Break-Fix Activity\n\n")
                mod_file.write("== Guided Steps\n")

        refined.write(f"include::{pages_dir}/{module}[leveloffset=+1]\n")

print(f"Refined AsciiDoc written to {output_file}")
