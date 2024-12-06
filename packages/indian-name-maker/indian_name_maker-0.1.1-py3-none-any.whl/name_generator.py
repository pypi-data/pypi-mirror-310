import os
import random
import pandas as pd
from typing import Optional

class NameGenerator:
    """A class to generate Indian names."""

    def __init__(self):
        """Initialize the NameGenerator with name data."""
        self._data_dir = "data"
        self._first_names = self._load_names("first_names.csv")
        self._last_names = self._load_names("last_names.csv")

    def _load_names(self, filename: str) -> list:
        """Load names from a CSV file.
        
        Args:
            filename: Name of the CSV file to load.
            
        Returns:
            List of names from the CSV file.
        """
        file_path = os.path.join(self._data_dir, filename)
        try:
            df = pd.read_csv(file_path, header=None)
            return df[0].str.capitalize().tolist()
        except Exception as e:
            raise RuntimeError(f"Error loading {filename}: {str(e)}")

    def get_first_name(self) -> str:
        """Generate a random first name.
        
        Returns:
            A random Indian first name.
        """
        return random.choice(self._first_names)

    def get_last_name(self) -> str:
        """Generate a random last name.
        
        Returns:
            A random Indian last name.
        """
        return random.choice(self._last_names)

    def get_full_name(self, separator: str = " ") -> str:
        """Generate a random full name.
        
        Args:
            separator: String to use between first and last name (default: " ").
            
        Returns:
            A random Indian full name.
        """
        return f"{self.get_first_name()}{separator}{self.get_last_name()}"

    def get_multiple_names(self, count: int = 1, full_name: bool = True) -> list:
        """Generate multiple random names.
        
        Args:
            count: Number of names to generate (default: 1).
            full_name: Whether to generate full names or just first names (default: True).
            
        Returns:
            List of generated names.
        """
        if count < 1:
            raise ValueError("Count must be greater than 0")

        return [
            self.get_full_name() if full_name else self.get_first_name()
            for _ in range(count)
        ]
