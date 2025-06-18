# Configuration file for the Sphinx documentation builder.

# -- Path setup --------------------------------------------------------------

from datetime import datetime
import os
import sys

import eml_urban_hydro_model as uhm

# -- Project information

project = "Urban Hydrological Model"

year_from = 2025
year_to = datetime.now().year
year_range = f"{year_from}-{year_to}" if year_from != year_to else str(year_from)
copyright = f"{year_range} EPFL (École Polytechnique Fédérale de Lausanne)"
author = "Yacine M'Hamdi, Son Pham-Ba"
__version__ = uhm.__version__
version = __version__
release = __version__

# -- General configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "myst_parser",
]


templates_path = ["_templates"]

autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "private-members": True,
}

# -- Options for HTML output

html_theme = "press"

# -- Options for MyST

myst_heading_anchors = 3

# -- Options for EPUB output
epub_show_urls = "footnote"


# -- Automatically run apidoc to generate rst from code
# https://github.com/readthedocs/readthedocs.org/issues/1139
def run_apidoc(_) -> None:
    from sphinx.ext.apidoc import main

    sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
    cur_dir = os.path.abspath(os.path.dirname(__file__))

    for module_dir in [
        "eml_urban_hydro_model",
    ]:
        module = os.path.join(cur_dir, "..", module_dir)
        output = os.path.join(cur_dir, "auto_source", module_dir)
        main(["-e", "-f", "-o", output, module])


def setup(app) -> None:
    app.connect("builder-inited", run_apidoc)
