#!/usr/bin/env python3
"""
Execute all notebooks in the repository (recursive) and export them to HTML into an output folder.

Usage:
  python scripts/build_notebooks.py <output_dir> [--timeout SECONDS]

By default this will search for all .ipynb files (excluding .ipynb_checkpoints) and:
- execute them with a timeout
- export resulting notebook to HTML and place the HTML in <output_dir> preserving folder structure
"""
import sys
import os
import subprocess
from pathlib import Path

def find_notebooks(root="."):
    nbs = []
    for p in Path(root).rglob("*.ipynb"):
        # skip checkpoints and files inside .git or site output
        if ".ipynb_checkpoints" in p.parts or "site" in p.parts or "gh-pages" in p.parts:
            continue
        nbs.append(p)
    return nbs

def main():
    if len(sys.argv) < 2:
        print("Usage: build_notebooks.py <output_dir> [--timeout SECONDS]")
        sys.exit(1)
    outdir = Path(sys.argv[1])
    timeout = 600
    if "--timeout" in sys.argv:
        try:
            timeout = int(sys.argv[sys.argv.index("--timeout")+1])
        except Exception:
            pass
    outdir.mkdir(parents=True, exist_ok=True)

    notebooks = find_notebooks(".")
    if not notebooks:
        print("No notebooks found.")
        return

    print(f"Found {len(notebooks)} notebooks. Exporting to {outdir} ...")
    for nb in notebooks:
        rel = nb.relative_to(Path.cwd())
        target_dir = outdir.joinpath(rel.parent)
        target_dir.mkdir(parents=True, exist_ok=True)
        print(f"Processing {nb} -> {target_dir}")

        # Execute notebook in place into a temp file and convert to HTML
        # Use nbconvert CLI to execute and export; capture exit code
        try:
            subprocess.check_call([
                sys.executable, "-m", "jupyter", "nbconvert",
                "--to", "html",
                "--execute",
                "--ExecutePreprocessor.timeout={}".format(timeout),
                "--output-dir", str(target_dir),
                str(nb)
            ])
        except subprocess.CalledProcessError as e:
            print(f"ERROR executing {nb}: {e}")
            # Create a placeholder HTML with the failure message so CI pages report which notebooks failed
            fail_html = target_dir.joinpath(nb.stem + ".html")
            with open(fail_html, "w", encoding="utf-8") as fh:
                fh.write(f"<html><body><h1>Execution failed for {nb}</h1><pre>{e}</pre></body></html>")
    print("Done.")

if __name__ == "__main__":
    main()
