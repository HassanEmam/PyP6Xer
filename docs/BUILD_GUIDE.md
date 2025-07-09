# PyP6Xer Documentation Build Guide

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r docs/requirements.txt
   ```

2. **Build documentation:**
   ```bash
   make docs
   ```

3. **Serve documentation locally:**
   ```bash
   make serve
   ```

## Documentation Structure

```
docs/
├── requirements.txt         # Documentation dependencies
├── source/                  # Source files
│   ├── index.md            # Main index page
│   ├── getting_started.md  # User guide
│   ├── examples.md         # Basic examples
│   ├── advanced_examples.md# Advanced usage
│   ├── troubleshooting.md  # Common issues
│   ├── contributing.md     # Developer guide
│   ├── changelog.md        # Version history
│   ├── license.md          # License information
│   ├── conf.py             # Sphinx configuration
│   └── api/                # API documentation (auto-generated)
│       ├── index.md        # API index
│       └── xerparser/      # Auto-generated API docs
└── build/                  # Built documentation
    ├── index.html          # Main page
    └── ...                 # Other generated files
```

## Available Make Commands

- `make help` - Show available commands
- `make install` - Install documentation dependencies
- `make docs` - Build HTML documentation
- `make clean` - Clean build files
- `make serve` - Build and serve documentation locally
- `make dev` - Start development server with auto-reload
- `make linkcheck` - Check for broken links
- `make pdf` - Build PDF documentation (requires LaTeX)

## Documentation Features

### Auto-Generated API Documentation
- Complete API reference using Sphinx AutoAPI
- Automatic documentation from docstrings
- Cross-references between modules and classes

### User-Friendly Features
- Modern responsive theme (Read the Docs)
- Copy-to-clipboard code buttons
- Search functionality
- Mobile-friendly navigation
- Syntax highlighting

### Content Organization
- **Getting Started**: Installation and basic usage
- **Examples**: Practical code examples
- **Advanced Examples**: Complex use cases and analysis
- **API Reference**: Complete class and method documentation
- **Troubleshooting**: Common issues and solutions
- **Contributing**: Development guidelines

## Building for Production

1. **Clean previous builds:**
   ```bash
   make clean
   ```

2. **Build documentation:**
   ```bash
   make docs
   ```

3. **Verify build:**
   ```bash
   make serve
   ```
   Open http://localhost:8000 to review

## Continuous Integration

The documentation can be automatically built and deployed using GitHub Actions or similar CI/CD systems:

```yaml
# Example GitHub Actions workflow
name: Build Documentation
on: [push, pull_request]
jobs:
  docs:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Setup Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.11'
    - name: Install dependencies
      run: pip install -r docs/requirements.txt
    - name: Build docs
      run: make docs
    - name: Deploy to GitHub Pages
      uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./docs/build/html
```

## Troubleshooting

### Common Issues

1. **Sphinx build errors:**
   - Check Python version compatibility
   - Verify all dependencies are installed
   - Check for syntax errors in .md files

2. **Missing API documentation:**
   - Ensure xerparser package is in Python path
   - Check autoapi_dirs setting in conf.py
   - Verify package imports work correctly

3. **Theme issues:**
   - Clear browser cache
   - Rebuild documentation completely
   - Check for CSS conflicts

### Getting Help

- Check the troubleshooting guide in the documentation
- Review Sphinx documentation
- Check project issues on GitHub

## Maintenance

### Regular Tasks
- Update examples when API changes
- Review and update troubleshooting guide
- Keep dependencies up to date
- Test documentation builds regularly

### Version Updates
- Update version in conf.py
- Update changelog.md
- Tag releases appropriately
- Update README badges if needed
