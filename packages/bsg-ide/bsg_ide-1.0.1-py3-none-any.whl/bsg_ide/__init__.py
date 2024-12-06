"""
Beamer Slide Generator IDE
A tool for creating Beamer presentations with multimedia support.
"""

from .BSG_IDE import BeamerSlideEditor
from .BeamerSlideGenerator import *

__version__ = "1.0.1"  # Incremented version number
__author__ = "Ninan Sajeeth Philip"
__email__ = "nsp@airis4d.com"

# This makes "import bsg_ide" load the main class
BeamerSlideIDE = BeamerSlideEditor
