"""Sphinx configuration."""

project = "singlecell-cookbook"
copyright = "2024, Argenis Arriojas"  # noqa: A001
author = "Argenis Arriojas"
release = "0.1.2"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx_autodoc_typehints",
    "myst_parser",
    "sphinx.ext.mathjax",  # Add MathJax support
]

templates_path = ["_templates"]
exclude_patterns = []
language = "en"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

# -- Extension configuration -------------------------------------------------
autodoc_typehints = "description"
autodoc_member_order = "bysource"

# Math options
mathjax3_config = {
    "tex": {
        "inlineMath": [["\\(", "\\)"]],
        "displayMath": [["\\[", "\\]"]],
    },
}
