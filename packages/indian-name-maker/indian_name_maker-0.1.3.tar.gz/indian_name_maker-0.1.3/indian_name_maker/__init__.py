"""Indian Name Maker - A package to generate Indian names."""

from indian_name_maker.name_generator import NameGenerator
from indian_name_maker.generator import get_multiple_first_names, get_multiple_full_names

__version__ = "0.1.3"
__all__ = [
    "NameGenerator",
    "get_multiple_first_names",
    "get_multiple_full_names"
]