import re
import os

# Define the input and output file paths
input_file = "nav.adoc"
output_file = "refined.adoc"

# Base directory for pages (assumed structure)
pages_dir = "pages"
os.makedirs(pages_dir, exist_ok=True)

# Read the original file
with open(input_file, "r") as file:
    content = file.read()

# Regex to match xrefs like `xref:module-01.adoc#bfxactivity[Break-Fix Activity]`
xref_pattern = r"\*\*\s*xref:(module-\d{2}\.adoc)(#[^\[]*)?\[(.*?)\]"

# Extract unique modules and prepare include statements
modules = set(re.findall(r"xref:(module-\d{2}\.adoc)", content))

# Write the refined AsciiDoc file
with open(output_file, "w") as refined:
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
