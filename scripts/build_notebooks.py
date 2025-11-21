#!/usr/bin/env python3
"""
Execute all notebooks in the repository (recursive) and export them to HTML into an output folder.

Usage:
  python scripts/build_notebooks.py <output_dir>

Example:
  python scripts/build_notebooks.py site/main
"""

import sys
import os
import glob
import subprocess


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/build_notebooks.py <output_dir>")
        sys.exit(1)

    output_dir = sys.argv[1]
    os.makedirs(output_dir, exist_ok=True)

    # Find all notebooks in the repository
    notebooks = glob.glob('**/*.ipynb', recursive=True)
    if not notebooks:
        print("No notebooks found.")
        # Create a simple index page
        index_path = os.path.join(output_dir, 'index.html')
        with open(index_path, 'w') as f:
            f.write("<html><body><h1>No notebooks found</h1></body></html>")
        sys.exit(0)

    print(f"Found {len(notebooks)} notebook(s)")

    # Execute and convert each notebook to HTML
    html_files = []
    for nb in notebooks:
        print(f"Processing: {nb}")
        try:
            # Execute the notebook
            subprocess.check_call([
                sys.executable, "-m", "jupyter", "nbconvert",
                "--to", "html",
                "--execute",
                "--ExecutePreprocessor.timeout=600",
                "--output-dir", output_dir,
                nb
            ])
            # Track the HTML file that was created
            nb_basename = os.path.basename(nb).replace('.ipynb', '.html')
            html_files.append(nb_basename)
            print(f"  ✓ Successfully converted: {nb}")
        except subprocess.CalledProcessError as e:
            print(f"  ✗ Failed to convert {nb}: {e}")
            # Create an error page
            error_html = os.path.join(
                output_dir, os.path.basename(nb).replace('.ipynb', '.html'))
            with open(error_html, 'w') as f:
                error_msg = f"<html><body><h1>Execution failed for {nb}</h1>"
                error_msg += f"<pre>{e}</pre></body></html>"
                f.write(error_msg)
            html_files.append(os.path.basename(error_html))

    # Create an index.html listing all notebooks
    index_path = os.path.join(output_dir, 'index.html')
    with open(index_path, 'w') as f:
        f.write("<html><head><title>Notebook Index</title></head><body>")
        f.write("<h1>Notebooks</h1>")
        f.write("<ul>")
        for html_file in sorted(html_files):
            f.write(f'<li><a href="{html_file}">{html_file}</a></li>')
        f.write("</ul>")
        f.write("</body></html>")

    print(f"\n✓ Build complete. Output in: {output_dir}")
    print(f"  Generated index: {index_path}")


if __name__ == "__main__":
    main()
