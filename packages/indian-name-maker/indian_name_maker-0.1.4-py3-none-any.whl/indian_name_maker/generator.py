"""High-level generator functions for indian-name-maker package."""

from indian_name_maker.name_generator import NameGenerator
from typing import List

# Create a single instance for reuse
_generator = NameGenerator()

def get_multiple_first_names(count: int = 1) -> List[str]:
    """Generate multiple first names.
    
    Args:
        count: Number of names to generate (default: 1)
        
    Returns:
        List of first names
        
    Raises:
        ValueError: If count is less than 1
    """
    return _generator.get_multiple_first_names(count)

def get_multiple_last_names(count: int = 1) -> List[str]:
    """Generate multiple last names.
    
    Args:
        count: Number of names to generate (default: 1)
        
    Returns:
        List of last names
        
    Raises:
        ValueError: If count is less than 1
    """
    return _generator.get_multiple_last_names(count)

def get_multiple_full_names(count: int = 1, separator: str = " ") -> List[str]:
    """Generate multiple full names.
    
    Args:
        count: Number of names to generate (default: 1)
        separator: String to use between first and last name (default: space)
        
    Returns:
        List of full names
        
    Raises:
        ValueError: If count is less than 1
    """
    return _generator.get_multiple_full_names(count, separator)
