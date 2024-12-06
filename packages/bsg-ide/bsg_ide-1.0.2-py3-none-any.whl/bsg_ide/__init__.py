"""
Beamer Slide Generator IDE
A tool for creating Beamer presentations with multimedia support.
"""

import os
import sys

# Add package directory to path
package_dir = os.path.dirname(os.path.abspath(__file__))
if package_dir not in sys.path:
    sys.path.insert(0, package_dir)

from .BSG_IDE import BeamerSlideEditor
from .BeamerSlideGenerator import *

__version__ = "1.0.2"
__author__ = "Ninan Sajeeth Philip"
__email__ = "nsp@airis4d.com"

def get_resource_path(filename):
    """Get full path to package resource file"""
    return os.path.join(package_dir, filename)
