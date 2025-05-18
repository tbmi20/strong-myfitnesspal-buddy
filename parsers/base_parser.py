from abc import ABC, abstractmethod
from typing import List, Any, Dict, TypeVar, Generic

T = TypeVar('T')  # Generic type for parsed data objects

class BaseParser(ABC, Generic[T]):
    """
    Abstract base class for data parsers
    """
    
    @abstractmethod
    def parse(self, file_path: str) -> List[T]:
        """
        Parse the data file and return a list of data objects
        
        Args:
            file_path: Path to the data file
            
        Returns:
            List of parsed data objects
        """
        pass