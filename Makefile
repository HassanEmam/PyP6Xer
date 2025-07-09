# Makefile for PyP6Xer Documentation

.PHONY: help docs clean install serve

# Default target
help:
	@echo "PyP6Xer Documentation Build System"
	@echo ""
	@echo "Available targets:"
	@echo "  install    Install documentation dependencies"
	@echo "  docs       Build HTML documentation"
	@echo "  clean      Clean build files"
	@echo "  serve      Serve documentation locally"
	@echo "  publish    Build and publish documentation"
	@echo "  help       Show this help message"

# Install documentation dependencies
install:
	@echo "Installing documentation dependencies..."
	pip install -r docs/requirements.txt
	@echo "Dependencies installed successfully!"

# Build documentation
docs:
	@echo "Building documentation..."
	cd docs && sphinx-build -b html source build/html
	@echo "Documentation built successfully!"
	@echo "Open docs/build/html/index.html to view"

# Clean build files
clean:
	@echo "Cleaning documentation build files..."
	rm -rf docs/build/
	rm -rf docs/source/api/xerparser/
	@echo "Clean complete!"

# Serve documentation locally
serve: docs
	@echo "Serving documentation at http://localhost:8000"
	cd docs/build/html && python -m http.server 8000

# Build for publication
publish: clean docs
	@echo "Documentation ready for publication in docs/build/html/"

# Development build with auto-reload
dev:
	@echo "Starting development server with auto-reload..."
	cd docs && sphinx-autobuild source build/html --host 0.0.0.0 --port 8000

# Check for broken links
linkcheck:
	@echo "Checking for broken links..."
	cd docs && sphinx-build -b linkcheck source build/linkcheck

# Build PDF documentation (requires LaTeX)
pdf:
	@echo "Building PDF documentation..."
	cd docs && sphinx-build -b latex source build/latex
	cd docs/build/latex && make
	@echo "PDF documentation built in docs/build/latex/"

# Check documentation syntax
doctest:
	@echo "Running documentation tests..."
	cd docs && sphinx-build -b doctest source build/doctest
