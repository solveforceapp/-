# Contributing

## CI/CD Workflows

This repository includes automated workflows for building, testing, and deploying Jupyter notebooks.

### CI Workflow (`.github/workflows/ci.yml`)

The CI workflow runs on every push and pull request to the `main` branch. It:

1. **Lints** the code using `flake8` to ensure code quality
2. **Runs unit tests** using `pytest` to validate functionality
3. **Executes all notebooks** to ensure they run without errors

To run these checks locally before pushing:

```bash
# Install dependencies
pip install -r requirements.txt

# Run linting
flake8 .

# Run tests
pytest -q --maxfail=1

# Execute notebooks
python scripts/build_notebooks.py /tmp/test-output
```

### Notebook Deployment Workflow (`.github/workflows/deploy-notebooks-pages.yml`)

The deployment workflow runs on every push to **any branch** and:

1. Executes all notebooks in the repository
2. Converts them to HTML
3. Publishes them to GitHub Pages under a branch-specific folder

The deployed notebooks are available at:
- `https://<username>.github.io/<repo>/<branch>/` for branch-specific builds
- `https://<username>.github.io/<repo>/` for an index of all published branches

### Building Notebooks Locally

To build notebooks locally for testing:

```bash
# Install dependencies
pip install -r requirements.txt

# Build notebooks to HTML
python scripts/build_notebooks.py output/

# View the generated HTML
open output/index.html  # macOS
xdg-open output/index.html  # Linux
```

### Adding New Notebooks

1. Create your `.ipynb` notebook file anywhere in the repository
2. Commit and push to your branch
3. The CI workflow will validate that the notebook executes successfully
4. The deployment workflow will automatically build and publish the notebook to GitHub Pages

### Troubleshooting

#### Notebook Execution Timeout

If a notebook takes longer than 600 seconds (10 minutes) to execute, you may need to:
- Optimize the notebook code
- Split it into smaller notebooks
- Increase the timeout in the workflow files

#### Flake8 Linting Errors

If you have Python code in the repository (not in notebooks), ensure it follows PEP 8 style guidelines:
- Maximum line length: 79 characters (default)
- Proper indentation and spacing
- No unused imports

To ignore certain flake8 errors, create a `.flake8` configuration file.
