
__version__ = '1.0.0'

# Import all functions from generator module (BeamerSlideGenerator)
from .generator import *

# Import main application
from .main import main

# Optional import for ODP conversion
try:
    from .odp import BeamerToODP
except ImportError:
    pass
