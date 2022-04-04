

from typing import Callable, Any
from Path import *
import outputtypes as out
import numpy as np

def TSP(algorithm: Callable, data, start:int , outputtype: out.OutputType=out.LengthAndRoute):
    path = outputtype.create_empty_path(data)
    algorithm(path, start)
    return outputtype.extract_output_from_path(path)

def randomWalk(path: Path,start:int, valueof: Callable[[Any], float] = lambda x:x):
    path.add_city_to_path(start, 0)
    NumOfCities=path.TotalCities
    curCity=start
    citiesToVisit=list(range(NumOfCities))
    citiesToVisit.remove(start) #permutation on the cities that we need to visit
    for i in np.random.permutation(citiesToVisit):
      path.add_city_to_path(i,path.dm[curCity][i])
      curCity=i   
    return path  

    


def greedy(path: Path,start:int, valueof: Callable[[Any], float] = lambda x:x):
    path.add_city_to_path(start, 0)#fix!
    NumOfCities=path.TotalCities
    curCity=start
    visitedIndexes=[start]
    for i in range(NumOfCities-1): #add the next city to the path (n-1) addings
        nextStep=2000
        index_of_closest_city=-1
        for j in range(NumOfCities): #find closest city to curCity
            if nextStep>path.dm[curCity][j] and j not in visitedIndexes:
                nextStep=path.dm[curCity][j]
                index_of_closest_city = j
        path.add_city_to_path(index_of_closest_city,nextStep) 
        visitedIndexes.append(index_of_closest_city)
        curCity=index_of_closest_city    
    return path     
       

    
    


if __name__ == "__main__":
    import doctest
    data=(["TLV","JLM","ETZ","YOK"],
        [[-1, 10, 15, 20],
        [10, -1, 35, 25], 
        [15, 35, -1, 30], 
        [20, 25, 30, -1]])
    
    print("input with names")
    print("length and route")
    print(TSP(greedy,data,1))
    print(TSP(randomWalk,data,1))
    print("length")
    print(TSP(greedy,data,1,out.Length))
    print(TSP(randomWalk,data,1,out.Length))
    print("route")
    print(TSP(greedy,data,1,out.Route))
    print(TSP(randomWalk,data,1,out.Route))

    data=([[-1, 10, 15, 20],
           [10, -1, 35, 25], 
           [15, 35, -1, 30], 
           [20, 25, 30, -1]])
    print("\ninput without names")
    print("length and route")
    print(TSP(greedy,data,1))
    print(TSP(randomWalk,data,1))
    print("lengths")
    print(TSP(greedy,data,1,out.Length))
    print(TSP(randomWalk,data,1,out.Length))
    print("route")
    print(TSP(greedy,data,1,out.Route))
    print(TSP(randomWalk,data,1,out.Route))
    
#output is:
#    
# input with names
# length and route
# (55, ['JLM', 'TLV', 'ETZ', 'YOK'])
# (70, ['JLM', 'YOK', 'ETZ', 'TLV'])
# length
# 55
# 60
# route
# ['JLM', 'TLV', 'ETZ', 'YOK']
# ['JLM', 'TLV', 'YOK', 'ETZ']
#
# input without names
# length and route
# (55, [1, 0, 2, 3])
# (70, [1, 3, 2, 0])
# lengths
# 55
# 55
# route
# [1, 0, 2, 3]
# [1, 3, 2, 0]