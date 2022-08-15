__version__ = '0.1.0'
__api__ = {
    'app': '0.1.0'
}

import os
import sys

# Add src/ folder to import discover path since Pyright/Pylance auto import
# generator often creates constructions like:
# `from app.some_module import some_obj`
# which is generating an import error.
sys.path.append(os.path.join(os.getcwd(), "src"))

from staze import Build, Service, View


build = Build(
    version=__version__,
    service_classes=[

    ],
    view_classes=[

    ],
)