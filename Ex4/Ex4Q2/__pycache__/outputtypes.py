"""
Define the various available output formats for a partition algorithm.
"""

from abc import ABC
from typing import Any, List
from Path import *


class OutputType(ABC):
    @classmethod
    def create_empty_path(cls):#) -> Path:
        """
        Construct and return a Path structure. Used at the initialization phase of an algorithm.
        """
        pass

    @classmethod
    def extract_output_from_path(cls, path: Path) -> Any:
        """
        Return the required output from the given path.
        """
        pass


class Length(OutputType):
    @classmethod
    def create_empty_path(cls, data):# -> List:
        return PathKeepingSum(data)

    # Output the total sum of the path
    @classmethod
    def extract_output_from_sums(cls, path:Path) :#-> List:
        return path.sum

    #Output the total sum of the path
    @classmethod
    def extract_output_from_path(cls, path: Path) -> List:
        return cls.extract_output_from_sums(path)




class Route(OutputType):
    @classmethod
    def create_empty_path(cls,data):# -> List:
        return PathKeepingContents(data)

    # Output the set of cities in path
    @classmethod
    def extract_output_from_path(cls, path: Path) :
        return path.route


class LengthAndRoute(Route):
    # Output the set of the path
    @classmethod
    def extract_output_from_path(cls, path: Path) :
        return (path.sum, path.route)