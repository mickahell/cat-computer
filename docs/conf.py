"""
Sphinx documentation builder
"""

# General options:
import os
import sys
from pathlib import Path

sys.path.append(os.path.abspath("../qat_computer"))

project = "QatComputer"
copyright = "2023"  # pylint: disable=redefined-builtin
author = "Michaël Rollin"

_rootdir = Path(__file__).parent.parent

# The full version, including alpha/beta/rc tags
release = "0.0.0"
# The short X.Y version
version = "0.0"

extensions = [
    "sphinx.ext.napoleon",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.mathjax",
    "sphinx.ext.viewcode",
    "sphinx.ext.extlinks",
    "jupyter_sphinx",
    "sphinx_autodoc_typehints",
    "reno.sphinxext",
    "nbsphinx",
    "sphinx_copybutton",
    "qiskit_sphinx_theme",
]
templates_path = ["_templates"]
numfig = True
numfig_format = {"table": "Table %s"}
language = "en"
pygments_style = "colorful"
add_module_names = False
modindex_common_prefix = ["qat_computer_project."]

# html theme options
html_theme = "qiskit-ecosystem"
html_title = f"{project} {release}"
#html_logo = "images/transparent_logo.png"
html_theme_options = {
    "sidebar_hide_name": False
}

# autodoc/autosummary options
autosummary_generate = True
autosummary_generate_overwrite = False
autoclass_content = "both"

# nbsphinx options (for tutorials)
nbsphinx_timeout = 180
nbsphinx_execute = "never"
nbsphinx_widgets_path = ""
nbsphinx_thumbnails = {
    "**": "_static/images/logo.png",
}

exclude_patterns = ["_build", "**.ipynb_checkpoints"]