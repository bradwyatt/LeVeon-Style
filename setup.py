# setup.py
from distutils.core import setup
import py2exe, sys

if len(sys.argv) == 1:
    sys.argv.append("py2exe")
    sys.argv.append("-q")
#replace windows with console if you want no console
setup(
    windows = [{'script': "LeVeon.py",
                "icon_resources": [(1, "leveonbell.ico")]}],
    version = "1.0",
    name = "Le'Veon Style",
    description = "Created by Brad Wyatt",
)