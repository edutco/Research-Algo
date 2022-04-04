

from abc import ABC, abstractmethod
from typing import Any, Callable


class Path(ABC):
    """
    An abstract path class.
    """

    def __init__(self, data=0):
        pass

    @abstractmethod
    def add_city_to_path(self, cityIndex, length:float):
        pass

    @abstractmethod
    def result(self):
        return None

class PathKeepingSum(Path):
    """
    A path structure that keeps track only of the total sum of the path
    """

    def __init__(self, data):
        super().__init__()
        self.sum=0
        if len(data)==2:
            self.dm=data=data[1]
        else:
            self.dm=data
        self.TotalCities=len(data)

    def add_city_to_path(self, cityIndex, length:float):
        self.sum += length

    def result(self):
        return self.sum

class PathKeepingContents(PathKeepingSum):
    """
    A path structure that keeps track of both the total sum of the path and the list of cities in the path
    """

    def __init__(self,data):
        self.route = []
        if len(data)==2:
            super().__init__(data[1])
            self.names=data[0]
        else:
            super().__init__(data)
            self.names=list(range(len(data)))  


    def add_city_to_path(self, cityIndex,length:float ):
        super().add_city_to_path(cityIndex,length )
        self.route.append(self.names[cityIndex])

    def result(self):
        return self.route

