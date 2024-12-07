# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import sys
import os

# sys.path.insert(0, os.path.abspath("."))
# sys.path.insert(0, os.path.abspath(".."))
sys.path.insert(0, os.path.abspath("../flit_demo"))


# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "flit_demo"
copyright = "2022, Exneyder A. Montoya-Araque"
author = "Exneyder A. Montoya-Araque"
release = "0.1.2"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.mathjax",
    "sphinx.ext.viewcode",
    "sphinx.ext.githubpages",
    "sphinx.ext.napoleon",
]

templates_path = ["_templates"]
exclude_patterns = []

# source_suffix = ['.rst', '.md']
source_suffix = ".rst"

# The master toctree document.
master_doc = "index"


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
