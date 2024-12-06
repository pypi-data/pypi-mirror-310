# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys

sys.path.insert(0, os.path.abspath("../"))

project = "epicure"
copyright = "2024, patillacode"
author = "patillacode"
release = "2024"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_autodoc_typehints",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# html_theme = "alabaster"
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_theme_options = {
    "style_external_links": True,
    "navigation_depth": 4,
}

# Add GitHub banner
html_context = {
    "display_github": True,  # Integrate GitHub
    "github_user": "patillacode",  # Username
    "github_repo": "epicure",  # Repo name
    "github_version": "main",  # Branch
    "conf_py_path": "/docs/",  # Path in the checkout to the docs root
}
