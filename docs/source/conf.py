"""
Sphinx configuration file for generating project documentation.

This file contains the configuration settings for building the documentation using Sphinx.
It includes project information, general configurations, and options for HTML output.
For more details on configuration options, refer to the Sphinx documentation:
https://www.sphinx-doc.org/en/master/usage/configuration.html

Attributes
----------
    project (str): The name of the project.
    copyright (str): The copyright information.
    author (str): The author's name.
    release (str): The release version of the project.
    extensions (list): The list of Sphinx extensions to be used.
    templates_path (list): Paths that contain templates.
    exclude_patterns (list): Patterns to exclude from the documentation.
    html_theme (str): The theme to use for HTML output.
    html_static_path (list): Paths that contain custom static files.

"""

import os
import sys

sys.path.insert(0, os.path.abspath("../../"))  # This adds the root directory to the path

# If the 'utils' directory is not directly under the root, adjust the path:
sys.path.insert(0, os.path.abspath("../../utils"))  # This adds the utils directory to the path

# Or add the directory explicitly
sys.path.insert(0, os.path.abspath("../../app"))


# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "TextTales"
copyright = "2024, Moritz Zewinger"
author = "Moritz Zewinger"
release = "0.0.0"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",  # For Google and NumPy style docstrings
    "sphinx.ext.viewcode",  # Add links to highlighted source code
]

templates_path = ["_templates"]
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
html_theme = "alabaster"
html_static_path = ["_static"]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "alabaster"
html_static_path = ["_static"]
