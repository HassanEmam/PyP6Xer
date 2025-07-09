# Contributing to PyP6Xer

We welcome contributions to PyP6Xer! This guide will help you get started with contributing to the project.

## Getting Started

### Development Setup

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/HassanEmam/PyP6Xer.git
   cd PyP6Xer
   ```

3. **Create a virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

4. **Install development dependencies**:
   ```bash
   pip install -e .
   pip install pytest pytest-cov sphinx sphinx-rtd-theme
   ```

### Development Workflow

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the coding standards below

3. **Write tests** for your changes

4. **Run the test suite**:
   ```bash
   pytest
   ```

5. **Update documentation** if needed

6. **Commit your changes**:
   ```bash
   git commit -m "Add feature: description of your feature"
   ```

7. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

8. **Create a Pull Request** on GitHub

## Coding Standards

### Code Style

- Follow [PEP 8](https://pep8.org/) Python style guidelines
- Use meaningful variable and function names
- Add docstrings to all public functions and classes
- Keep functions focused and modular

### Documentation

- Use Google-style docstrings:
  ```python
  def function_name(param1: str, param2: int) -> bool:
      """Brief description of the function.
      
      Longer description if needed.
      
      Args:
          param1: Description of param1
          param2: Description of param2
          
      Returns:
          Description of return value
          
      Raises:
          ValueError: Description of when this is raised
      """
  ```

- Update relevant documentation files when adding features
- Include examples in docstrings where helpful

### Testing

- Write unit tests for new functionality
- Ensure tests cover edge cases
- Use descriptive test names
- Aim for high test coverage

Example test structure:
```python
def test_reader_loads_basic_xer_file():
    """Test that Reader can load a basic XER file."""
    reader = Reader("test_data/sample.xer")
    assert reader.projects.count > 0
    assert len(reader.activities) > 0
```

## Types of Contributions

### Bug Reports

When reporting bugs, please include:

- Description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Python version and OS
- Sample XER file (if possible and not confidential)

### Feature Requests

For new features, please:

- Describe the use case
- Explain why it would be valuable
- Provide examples of how it would be used
- Consider the scope and complexity

### Code Contributions

We welcome:

- Bug fixes
- New XER element support
- Performance improvements
- Documentation improvements
- Test coverage improvements
- Example scripts and tutorials

### Documentation

Help improve documentation by:

- Fixing typos and grammar
- Adding examples
- Improving clarity
- Adding missing documentation
- Translating documentation

## Project Structure

Understanding the codebase structure:

```text
PyP6Xer/
├── xerparser/              # Main package
│   ├── __init__.py        # Package imports
│   ├── reader.py          # Main XER file reader
│   ├── write.py           # XER file writer
│   ├── model/             # Data model classes
│   │   ├── classes/       # Individual entity classes
│   │   │   ├── project.py # Project class
│   │   │   ├── task.py    # Task/Activity class
│   │   │   ├── resource.py# Resource class
│   │   │   └── ...        # Other classes
│   │   ├── projects.py    # Projects collection
│   │   ├── tasks.py       # Tasks collection
│   │   └── ...            # Other collections
│   └── dcma14/            # DCMA 14-point analysis
├── tests/                 # Test suite
├── docs/                  # Documentation
├── sample.xer            # Sample XER file
├── setup.py              # Package setup
└── README.md             # Project README
```

## Adding New XER Elements

To add support for a new XER element type:

1. **Create the class** in `xerparser/model/classes/`:
   ```python
   class NewElement:
       def __init__(self, params):
           self.element_id = params.get('element_id')
           # ... other properties
           
       def get_tsv(self):
           # Return TSV representation
           return ["%R", self.element_id, ...]
   ```

2. **Create the collection class** in `xerparser/model/`:
   ```python
   class NewElements:
       def __init__(self):
           self._elements = []
           
       def add(self, params):
           self._elements.append(NewElement(params))
   ```

3. **Update the Reader class** to parse the new element:
   ```python
   elif object_type.strip() == "NEWELEMENT":
       self._new_elements.add(params)
   ```

4. **Add property to Reader** for accessing the collection:
   ```python
   @property
   def new_elements(self):
       return self._new_elements
   ```

5. **Update imports** in `__init__.py`

6. **Write tests** for the new functionality

7. **Update documentation**

## Release Process

For maintainers:

1. Update version in `setup.py`
2. Update `CHANGELOG.md`
3. Create a git tag: `git tag v1.x.x`
4. Push tag: `git push origin v1.x.x`
5. Create GitHub release
6. Publish to PyPI:
   ```bash
   python setup.py sdist bdist_wheel
   twine upload dist/*
   ```

## Questions?

- Open an issue for bugs or feature requests
- Start a discussion for questions about the codebase
- Contact the maintainers for security issues

Thank you for contributing to PyP6Xer!
