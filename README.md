# Repository: Notebook pages (branch-per-branch)

This repository contains many Jupyter notebooks. This change adds CI and an automated build-and-deploy workflow that runs on pushes to any branch and publishes rendered HTML pages for that branch under gh-pages/<branch-name>.

Files added:
- .github/workflows/ci.yml — runs lint/tests and executes notebooks on pushes/PRs to main.
- .github/workflows/deploy-notebooks-pages.yml — builds and deploys per-branch HTML pages to gh-pages when any branch is pushed.
- scripts/build_notebooks.py — script that executes notebooks and exports them to HTML.
- requirements.txt, Dockerfile, .pre-commit-config.yaml, .gitignore — tooling and environment files.

How to run locally:
1. python -m venv .venv
2. source .venv/bin/activate
3. pip install -r requirements.txt
4. python scripts/build_notebooks.py site/local-branch

Enable GitHub Pages to serve the gh-pages branch in repository Settings -> Pages. The per-branch pages will be available at https://<owner>.github.io/<repo>/<branch>/ .
