# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
import sphinx_rtd_theme
sys.path.insert(0, os.path.abspath('..'))


# -- Project information -----------------------------------------------------

project = 'Cartograph'
copyright = '2019, Alastair Flynn'
author = 'Alastair Flynn'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.autodoc', 'sphinx_rtd_theme']
autodoc_member_order = 'bysource'

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'classic'
html_theme_options = {'linkcolor':'#000099', 'visitedlinkcolor':'#000099', 'sidebarlinkcolor':'#000099', 'relbarlinkcolor':'#000099',
'bgcolor':'#ffffff', 'footerbgcolor':'#dddddd', 'headbgcolor':'#ffffff', 'sidebarbgcolor':'#ffffff', 'relbarbgcolor':'#dddddd',
'textcolor':'#121212', 'footertextcolor':'#121212', 'headtextcolor':'#121212', 'sidebartextcolor':'#121212', 'relbartextcolor':'#121212'}
# 'codebgcolor':'#121212', 'codetextcolor':'#aaaaaa'}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']