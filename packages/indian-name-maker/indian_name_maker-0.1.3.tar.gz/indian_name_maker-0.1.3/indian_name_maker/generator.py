"""High-level functions for generating Indian names."""

from indian_name_maker.name_generator import NameGenerator
from typing import List

# Create a single instance for reuse
_generator = NameGenerator()

def get_multiple_first_names(count: int = 1) -> List[str]:
    """Generate multiple random first names efficiently.
    
    Args:
        count: Number of first names to generate (default: 1)
        
    Returns:
        List of first names
        
    Raises:
        ValueError: If count is less than 1
    """
    return _generator.get_first_names(count)

def get_multiple_full_names(count: int = 1, separator: str = " ") -> List[str]:
    """Generate multiple random full names efficiently.
    
    Args:
        count: Number of full names to generate (default: 1)
        separator: String to use between first and last name (default: space)
        
    Returns:
        List of full names
        
    Raises:
        ValueError: If count is less than 1
    """
    return _generator.get_full_names(count, separator)
