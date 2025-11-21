#!/usr/bin/env python3
"""
Execute all notebooks in the repository (recursive) and export them to HTML into an output folder.

Usage:
  python scripts/build_notebooks.py <output_dir>
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

    # Find all notebooks recursively
    notebooks = glob.glob('**/*.ipynb', recursive=True)
    # Exclude notebooks in output_dir if it's a subdirectory
    notebooks = [nb for nb in notebooks if not nb.startswith(output_dir)]

    if not notebooks:
        print("No notebooks found.")
        # Create a placeholder index
        index_path = os.path.join(output_dir, 'index.html')
        with open(index_path, 'w') as f:
            f.write("<html><body><h1>No notebooks found</h1></body></html>")
        sys.exit(0)

    print(f"Found {len(notebooks)} notebook(s)")

    results = []
    for nb in notebooks:
        print(f"Processing {nb}...")
        # Determine output HTML path
        html_name = os.path.basename(nb).replace('.ipynb', '.html')
        html_path = os.path.join(output_dir, html_name)
        
        try:
            # Execute and convert to HTML
            subprocess.check_call([
                sys.executable, "-m", "jupyter", "nbconvert",
                "--to", "html",
                "--execute",
                "--ExecutePreprocessor.timeout=600",
                "--output", html_path,
                nb
            ])
            print(f"  -> {html_path}")
            results.append((nb, html_name, True, None))
        except subprocess.CalledProcessError as e:
            print(f"  FAILED: {e}")
            # Create an error page
            with open(html_path, 'w') as f:
                f.write(f"<html><body><h1>Execution failed for {nb}</h1><pre>{e}</pre></body></html>")
            results.append((nb, html_name, False, str(e)))

    # Create index.html listing all notebooks
    index_path = os.path.join(output_dir, 'index.html')
    with open(index_path, 'w') as f:
        f.write("<html><head><title>Notebooks</title></head><body>")
        f.write("<h1>Notebooks</h1><ul>")
        for nb, html_name, success, error in results:
            status = "✓" if success else "✗"
            f.write(f'<li>{status} <a href="{html_name}">{nb}</a>')
            if not success:
                f.write(f' <span style="color:red">(failed)</span>')
            f.write('</li>')
        f.write("</ul></body></html>")
    
    print(f"\nIndex created at {index_path}")
    print(f"Successfully built {sum(1 for _, _, s, _ in results if s)}/{len(results)} notebooks")

if __name__ == "__main__":
    main()
