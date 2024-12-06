"""Core functionality for generating Indian names."""

import os
import numpy as np
import pandas as pd
from pathlib import Path
from typing import List, Union

class NameGenerator:
    """A class to generate Indian names."""
    
    # Class-level cache for names
    _first_names_cache = None
    _last_names_cache = None
    
    def __init__(self):
        """Initialize the NameGenerator with name data."""
        # Use class-level cache if available
        if NameGenerator._first_names_cache is None:
            NameGenerator._first_names_cache = self._load_names("first_names.csv", "FirstName")
        if NameGenerator._last_names_cache is None:
            NameGenerator._last_names_cache = self._load_names("last_names.csv", "LastName")
        
        # Create numpy random generator for faster random selection
        self._rng = np.random.default_rng()

    def _load_names(self, filename: str, column_name: str) -> np.ndarray:
        """Load names from a CSV file into a numpy array."""
        try:
            current_dir = Path(__file__).parent
            data_path = current_dir / 'data' / filename
            if not data_path.exists():
                raise FileNotFoundError(f"Could not find {filename} in {data_path}")
            
            df = pd.read_csv(data_path, encoding='utf-8')
            return df[column_name].to_numpy()
        except Exception as e:
            raise RuntimeError(f"Error loading {filename}: {str(e)}")

    def get_first_name(self) -> str:
        """Get a single random first name."""
        return self._rng.choice(NameGenerator._first_names_cache)

    def get_last_name(self) -> str:
        """Get a single random last name."""
        return self._rng.choice(NameGenerator._last_names_cache)

    def get_full_name(self, separator: str = " ") -> str:
        """Get a single random full name."""
        return f"{self.get_first_name()}{separator}{self.get_last_name()}"

    def get_multiple_first_names(self, count: int) -> List[str]:
        """Get multiple random first names efficiently.
        
        Args:
            count: Number of names to generate
            
        Returns:
            List of first names
            
        Raises:
            ValueError: If count is less than 1
        """
        if count < 1:
            raise ValueError("Count must be greater than 0")
        return self._rng.choice(NameGenerator._first_names_cache, size=count).tolist()

    def get_multiple_last_names(self, count: int) -> List[str]:
        """Get multiple random last names efficiently.
        
        Args:
            count: Number of names to generate
            
        Returns:
            List of last names
            
        Raises:
            ValueError: If count is less than 1
        """
        if count < 1:
            raise ValueError("Count must be greater than 0")
        return self._rng.choice(NameGenerator._last_names_cache, size=count).tolist()

    def get_multiple_full_names(self, count: int, separator: str = " ") -> List[str]:
        """Get multiple random full names efficiently.
        
        Args:
            count: Number of names to generate
            separator: String to use between first and last name
            
        Returns:
            List of full names
            
        Raises:
            ValueError: If count is less than 1
        """
        if count < 1:
            raise ValueError("Count must be greater than 0")
        
        first_names = self.get_multiple_first_names(count)
        last_names = self.get_multiple_last_names(count)
        return [f"{first}{separator}{last}" for first, last in zip(first_names, last_names)]
