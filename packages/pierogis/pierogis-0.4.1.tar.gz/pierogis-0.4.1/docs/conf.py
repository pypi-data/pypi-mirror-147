import os
import sys

from importlib_metadata import version

sys.path.insert(0, os.path.abspath('../src'))

# Project --------------------------------------------------------------

project = "pierogis"
copyright = "2021 pierogis"
author = "pierogis-live"
version = version('pierogis')

# General --------------------------------------------------------------

master_doc = "index"
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinxcontrib.apidoc',
    'sphinx_issues',
    'sphinx.ext.viewcode'
]
intersphinx_mapping = {
    "rich": ("https://rich.readthedocs.io/en/stable/", None),
    "imageio": ("https://imageio.readthedocs.io/en/stable/", None),
    "Pillow": ("https://pillow.readthedocs.io/en/stable/", None),
    'python': ('https://docs.python.org/3', None),
}
issues_github_path = "pierogis/pierogis"
apidoc_module_dir = '../src/pierogis'
apidoc_output_dir = 'source'
apidoc_separate_modules = True

# HTML -----------------------------------------------------------------

html_theme = "alabaster"
html_sidebars = {
    '**': [
        'about.html',
        'navigation.html',
        'relations.html',
        'searchbox.html',
    ]
}
html_title = f"pierogis docs ({version})"
html_show_sourcelink = True
html_theme_options = {
    "description": "image and animation processing framework",
    "github_user": "pierogis",
    "github_repo": "pierogis",
    "fixed_sidebar": True,
    'github_type': ''
}
