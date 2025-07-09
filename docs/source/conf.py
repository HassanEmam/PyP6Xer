# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
sys.path.insert(0, os.path.abspath('../../'))

project = 'PyP6Xer'
copyright = '2020-2025, Hassan Emam'
author = 'Hassan Emam'
release = '1.015.00'
version = '1.015.00'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
    'sphinx.ext.coverage',
    'sphinx.ext.githubpages',
    'autoapi.extension',
    'myst_parser',
    'sphinx_copybutton',
]

# AutoAPI settings
autoapi_type = 'python'
autoapi_dirs = ['../../xerparser']
autoapi_root = 'api'
autoapi_add_toctree_entry = False
autoapi_options = [
    'members',
    'undoc-members',
    'show-inheritance',
    'show-module-summary',
    'special-members',
    'imported-members',
]

# Napoleon settings for Google/NumPy style docstrings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_preprocess_types = False
napoleon_type_aliases = None
napoleon_attr_annotations = True

# Autodoc settings
autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': True,
    'exclude-members': '__weakref__'
}

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_title = f'{project} v{version}'
html_short_title = project

# Theme options
html_theme_options = {
    'logo_only': False,
    'display_version': True,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': False,
    'vcs_pageview_mode': '',
    'style_nav_header_background': '#2980B9',
    # Toc options
    'collapse_navigation': True,
    'sticky_navigation': True,
    'navigation_depth': 4,
    'includehidden': True,
    'titles_only': False
}

# Intersphinx mapping
intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
}

# Source file suffixes
source_suffix = ['.rst', '.md']

# MyST parser configuration
myst_enable_extensions = [
    "deflist",
    "tasklist",
    "fieldlist",
    "attrs_inline",
    "colon_fence",
]

# Master document
master_doc = 'index'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
if not os.path.exists('_static'):
    os.makedirs('_static')

# Copy button configuration
copybutton_prompt_text = r">>> |\.\.\. |\$ |In \[\d*\]: | {2,5}\.\.\.: | {5,8}: "
copybutton_prompt_is_regexp = True
copybutton_only_copy_prompt_lines = True

# Syntax highlighting
pygments_style = 'sphinx'
highlight_language = 'python'

# Linkcheck settings
linkcheck_ignore = [
    r'http://localhost.*',
    r'https://github\.com/.*/issues$',  # GitHub issues redirects
    r'.*\.local.*',
    r'https://github\.com/yourusername/.*',  # Ignore template URLs
]
linkcheck_timeout = 10
linkcheck_retries = 3
linkcheck_anchors_ignore = [
    r'filtering-data',  # Ignore anchor check issues
]

# Suppress specific warnings
suppress_warnings = [
    'misc.highlighting_failure',  # Suppress highlighting failures for text blocks
]
