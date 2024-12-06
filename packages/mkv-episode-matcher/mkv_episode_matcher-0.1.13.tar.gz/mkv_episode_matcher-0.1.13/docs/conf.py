# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import sys
import os
sys.path.insert(0, os.path.abspath('..'))
# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'MKV Episode Matcher'
copyright = '2024, Jonathan Sakkos'
author = 'Jonathan Sakkos'
release = '0.1.5'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.napoleon',    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',   'sphinx.ext.autosummary','sphinx.ext.coverage']

napoleon_google_docstring = True
napoleon_use_param = False
napoleon_use_ivar = True

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'#furo
html_static_path = ['_static']
