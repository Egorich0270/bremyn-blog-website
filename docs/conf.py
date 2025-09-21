import os, sys
import tomllib as tl # если Python <3.11 pip install tomli


sys.path.insert(0, os.path.abspath("../src"))

with open(os.path.join(os.path.dirname(__file__), "..", "pyproject.toml"), "rb") as f:
    pyproject = tl.load(f)

project = pyproject["project"]["name"]
author = ", ".join(pyproject["project"].get("authors", [{"name": "Unknown"}])[0].values())
release = pyproject["project"]["version"]

extensions = [
    "sphinx.ext.autodoc",      # Автодоки из docstrings
    "sphinx.ext.napoleon",     # Поддержка Google-style и NumPy-style докстрингов
]

templates_path = ["_templates"]
exclude_patterns = []

html_theme = "sphinx_rtd_theme"

rst_epilog = f"""
.. |project| replace:: {project}
.. |author| replace:: {author}
.. |release| replace:: {release}
"""
