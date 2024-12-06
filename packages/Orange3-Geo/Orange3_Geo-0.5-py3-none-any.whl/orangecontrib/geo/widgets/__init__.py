from orangecanvas.utils.localization.si import plsi, plsi_sz, z_besedo
from orangecanvas.utils.localization import Translator  # pylint: disable=wrong-import-order
_tr = Translator("orangecontrib.geo", "biolab.si", "Orange")
del Translator
# Category metadata.

NAME = "Geo"
DESCRIPTION = _tr.m[10, "Transformation and visualization of geographical data."]

# Category icon show in the menu
ICON = "icons/category.svg"

# Background color for category background in menu
# and widget icon background in workflow.
BACKGROUND = "#a0eaa0"

# Location of widget help files.
WIDGET_HELP_PATH = (
    # Used for development.
    # You still need to build help pages using
    # make html
    # inside doc folder
    ("{DEVELOP_ROOT}/doc/_build/html/index.html", None),

    # Online documentation url, used when the local documentation is available.
    # Url should point to a page with a section Widgets. This section should
    # includes links to documentation pages of each widget. Matching is
    # performed by comparing link caption to widget name.
    ("http://orange3-geo.readthedocs.io/en/latest/", "")
)
