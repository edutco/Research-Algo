

from cgitb import small
from itertools import repeat
import math

from typing import Callable
from typing import List
import concurrent.futures
from numpy import append, number, obj2sctype as obj

from prtpy import bins
from prtpy import objectives as obj, Bins, partitioning

from prtpy.bins import BinsKeepingContents

from prtpy.bins import BinsKeepingSums



from heapq import heapreplace



def sublist_creator(x, n, sort=True):
    bins = [[0] for _ in range(n)]
    if sort:
        x = sorted(x, key = ValOf)
    # if isinstance(x[0], int):
    #     for job in x:
    #         least = bins[0]
    #         least[0] += job
    #         least.append(job)
    #         heapreplace(bins, least)
    # else:
    #     for (i, job) in x:
    #         least = bins[0]
    #         least[0] += job
    #         least.append((i,job))
    #         heapreplace(bins, least)  
    for job in x:
            least = bins[0]
            least[0] += ValOf(job)
            least.append(job)
            heapreplace(bins, least)                 

    return [x[1:] for x in bins]

def CalcLambda_star(f:Callable,epsilon:float)->int:
    """
     "this algo calculate delte and lambda start given an epsilon and f
     >>> CalcLambda_star(lambda x:x , 0.1)
     50
     >>> CalcLambda_star(lambda x:x**2 , 0.1)
     103
     >>> CalcLambda_star(lambda x:x**1.1 , 0.1)
     56
     >>> CalcLambda_star(lambda x:x**2 , 0.5)
     23
     """
    fPower=math.log2(f(2))
    delta=(1+epsilon)**(1.0/fPower)-1        
    lambda_star=int(math.ceil(5.0/delta))
    # if lambda_star>100:
    #     print("Warning!! \nthis example is too big for this computer")
    return lambda_star    

def ValOf(x):
    """
     "this algo calculate value of job. if job is int it return the int' if it is tuple of (index,val) it returns val
     >>> ValOf(8)
     8
     >>> ValOf(20)
     20
     >>> ValOf((1,58))
     58
     >>> ValOf(("a",67))
     67
     """
    if isinstance(x,int):
        return x
    if isinstance(x,float):
        return x    
    else:
        return x[1]    
def mainAlgorithm( bins: Bins, #bin is a machine
                    items: List[any], #item jobs
                    epsilon :float,
                    f:Callable= lambda x: x,#the f function we use to calculate completion time
                    valueof: Callable = ValOf, 
                    )->List[List[int]]:
    """
    "Approximation Schemes for Scheduling on Parallel Machines", by Noga Alon, Yossi Azar, Gerhard J. Woeginger and Tal Yadid,
     (1975), https://onlinelibrary.wiley.com/doi/10.1002/(SICI)1099-1425(199806)1:1%3C55::AID-JOS2%3E3.0.CO;2-J
    main algorithm in the artical (page.9): accepts List of jobs and number of machines 
    and creates a schedule for the machines s.t, we process all the jobs and minimize sum(f(C_i)) 
    when C_i is the compilition time of machine #i (0<i<number_of_machines+1)
    f(x) is a given convex function.
    the gerenteed result is that the diffenence between the algorithm output and the optimal schedul (that minimize sum(f(C_i)) )
    is <= epsilon * OPT"
    >>> mainAlgorithm(BinsKeepingContents(3),[100,100,10,50],0.1, lambda x:x**2,ValOf)
    Bin #0: [(1, 100)], sum=100.0
    Bin #1: [(2, 100)], sum=100.0
    Bin #2: [(3, 10), (4, 50)], sum=60.0
    >>> mainAlgorithm(BinsKeepingContents(2),[10,10,10],0.1, lambda x:x**2,ValOf)
    Bin #0: [(1, 10), (2, 10)], sum=20.0
    Bin #1: [(3, 10)], sum=10.0
    Example 1: 
    >>> mainAlgorithm(BinsKeepingContents(2),[124000,34000,54768,115256,89765,43124,107,23047,200101,78900,65432,101436,52422,17642],0.1,lambda x:x**2)
    Bin #0: [(2, 34000), (11, 65432), (10, 78900), (1, 124000), (9, 200101)], sum=502433.0
    Bin #1: [(14, 17642), (8, 23047), (6, 43124), (13, 52422), (3, 54768), (5, 89765), (12, 101436), (4, 115256), (7, 107)], sum=497567.0
    """    

    # Example 2: 
    # >>> mainAlgorithm(0.5,[426,666,846,8500,3300,1546,985,103,674,131,124,564,135],2,lambda x:x)
    # [[426,666,846,8500,3300,1546,985,103,674,131,124,564,135][]]

    # Example 3:
    # >>> mainAlgorithm(0.5,[107,7502,684,12123,450,4663,1985,4102,1052,407,310,113,200,23,1012,41,126,5100],4,lambda x:x**2)
    # [[107,4663,1985,4102,407,113],[7502,23,1012,41,5100],[684,450,1052,310,200,126],[12123]]

    bins.set_valueof(ValOf)                
    if isinstance(items[0],int):
        items=list(enumerate(items,1))
    Finalpartition=[]          
    lambda_star=CalcLambda_star(f,epsilon)       
    jobsSum=0
    for item in items:
        jobsSum+=valueof(item)
    L=jobsSum/bins.num
    fullBins = [False] * bins.num
    numOfFullBins=0
    for (i,job) in items[:]:
        if job>=L:
            items.remove((i,job))
            index_of_least_full_bin = min(range(bins.num), key=bins.sums.__getitem__)
            bins.add_item_to_bin((i,job), index_of_least_full_bin)
            fullBins[index_of_least_full_bin]=True
            Finalpartition.append([(i,job)])
            numOfFullBins+=1

    CJ, SJ=ConvertJobs(items,L,lambda_star)   
    partition=IP(CJ,bins.num-numOfFullBins,valueof)
    ans=deconvertJobs(items, partition,L,lambda_star,SJ)
    for machine in ans:
        Finalpartition.append(machine)
        for job in machine:
            bins.add_item_to_bin(job,numOfFullBins)
        numOfFullBins+=1    
    return bins

def addSmallJob(set, job,value, index=0):
    if isinstance(job,int):
        set.append(value) 
    else:    
        if index==0:
            set.append((job[0],value)) 
        else:
            set.append((index,value))     

def addBigJob(set, job, value):
    if isinstance(job,int):
        set.append(value) 
    else:    
        set.append((job[0],value))         

def ConvertJobs(jobs: List[any], L: int, lambda_star:int, Valueof:Callable=ValOf):#returns two things
    """
    "this algorithm convert every job p_j to its corresponding job p_j#
    >>> ConvertJobs([124000,34000,54768,115256,89765,43124,107,23047,200101,78900,65432,101436,52422,17642],500000,500)
    ([124000.0, 34000.0, 54768.0, 115256.0, 89766.0, 43124.0, 23048.0, 200102.0, 78900.0, 65432.0, 101436.0, 52422.0, 17642.0, 1000.0], [107])
    >>> ConvertJobs([100,200,300,400],500,500)
    ([100.0, 200.0, 300.0, 400.0], [])
    >>> ConvertJobs([1,2,3,4],5,2)
    ([3.75, 5.0, 2.5, 2.5], [1, 2])
    >>> ConvertJobs([(1,1),(2,2),(3,3),(4,4)],5,2)
    ([(3, 3.75), (4, 5.0), (-1, 2.5), (-1, 2.5)], [(1, 1), (2, 2)])
    >>> ConvertJobs([(1,1),(2,1),(3,3),(4,4)],7,2)
    ([(4, 5.25), (-1, 3.5), (-1, 3.5)], [(1, 1), (2, 1), (3, 3)])
    """
    convertedSet=[]
    communMultiple=L/(lambda_star**2)
    smallJobs=[]
    LdivLambda=L/lambda_star       
    S=0 #total sum of small jobs
    for job in jobs:
        if Valueof(job)>= LdivLambda: #big job
            newJob=math.ceil(Valueof(job)/communMultiple)*communMultiple
            addBigJob(convertedSet,job,newJob)
        else:    #small job
            S+=Valueof(job) 
            addSmallJob(smallJobs,job,Valueof(job)) 
    NumNewSmallJobs=int(math.ceil(S/LdivLambda))       
    for i in range(NumNewSmallJobs):
        addSmallJob(convertedSet, job,LdivLambda,-1) 
    return convertedSet,smallJobs    

def numberToBase(n, b, length):
    if n == 0:
        return "0"*length
    digits = ""
    while n:
        digits+=str(int(n % b))#.append(int(n % b))
        n //= b
    if len(digits)<length: 
        digits="0"*(-len(digits)+length)+digits   
    return digits#[::-1]

def calculateMaxInDiv(curDiv,base, jobs):
    makespan=[0]*base
    jobList=a = [[] for x in repeat(None, base)]
    for i in range(len(jobs)):
        makespan[int(curDiv[i])]+=ValOf(jobs[i])
        jobList[int(curDiv[i])].append(jobs[i])
    return (max(makespan),jobList)    

def loopForDivision(start,end, base, jobs):
    curMin=float("inf")
    minDiv=[]
    for i in range(start,end):
        curDiv=numberToBase(i,base,len(jobs))
        divResult=calculateMaxInDiv(curDiv,base,jobs)
        if divResult[0]<curMin:
            curMin=divResult[0]
            minDiv=divResult[1]
    return(curMin,minDiv)        

def IP(convertedJobs: List[float], numbrOfMachines:int, f: Callable)->List[List[float]]:
    #this function does not work yet!!!!!!!!!
    """
    "partition the  converted jobs into numbrOfMachines parts in an optimal way such that we minimize sum(f(C_i))"
    >>> IP([10,15,10,10,15],2,lambda x:x**2)
    [[10, 10, 10], [15, 15]]
    """
    divisions=numbrOfMachines**len(convertedJobs)
    # t1 = threading.Thread(target = loopForDivision ,args = [0,int(divisions/4), numbrOfMachines, convertedJobs] )
    # t2 = threading.Thread(target = loopForDivision ,args = [int(divisions/4),int(divisions/2), numbrOfMachines, convertedJobs] )
    # t3 = threading.Thread(target = loopForDivision ,args = [int(divisions/2),int(divisions/4)*3, numbrOfMachines, convertedJobs] )
    # t4 = threading.Thread(target = loopForDivision ,args = [int(divisions/4)*3,divisions, numbrOfMachines, convertedJobs] )

    with concurrent.futures.ThreadPoolExecutor(8) as exect:
        results =[ exect.submit(loopForDivision , 0,                 int(divisions/8), numbrOfMachines, convertedJobs) ,
                   exect.submit(loopForDivision , int(divisions/8),  int(divisions/4), numbrOfMachines, convertedJobs),
                   exect.submit(loopForDivision , int(divisions/4),  int(divisions/8)*3, numbrOfMachines, convertedJobs),
                   exect.submit(loopForDivision , int(divisions/8)*3,int(divisions/2), numbrOfMachines, convertedJobs),
                   exect.submit(loopForDivision , int(divisions/2),  int(divisions/8)*5,numbrOfMachines, convertedJobs) ,
                   exect.submit(loopForDivision , int(divisions/8)*5,int(divisions/8)*6, numbrOfMachines, convertedJobs),
                   exect.submit(loopForDivision , int(divisions/8)*6,int(divisions/8)*7, numbrOfMachines, convertedJobs),
                   exect.submit(loopForDivision , int(divisions/8)*7,divisions, numbrOfMachines, convertedJobs)
        ]
        curMin=float("inf")
        minDiv=[]
        for res in concurrent.futures.as_completed(results):
            if res.result()[0]<curMin:
                curMin=res.result()[0]
                minDiv=res.result()[1]

    # curMin=float("inf")
    # for i in range(numbrOfMachines**len(convertedJobs)):
    #     curDiv=numberToBase(i,numbrOfMachines,len(convertedJobs))
    #     divResult=calculateMaxInDiv(curDiv,numbrOfMachines,convertedJobs)
    #     if divResult[0]<curMin:
    #         curMin=divResult[0]
    #         minDiv=divResult[1]
    # >>> IP([124000,34000,54768,115256,89766,43124,1000,23048,200102,78900,65432,101436,52422,17642],2,lambda x:x**2)
    # [[124000,54768,89766,78900,101436,52422,17642],[34000,115256,43124,1000,23048,200102,65432]]
    #partition=sublist_creator(convertedJobs,numbrOfMachines)
    # print("partition",partition)

    return minDiv


def deconvertJobs(originalJobs,partition: List[List[any]], L: float, lambda_star:int, SmallJobs:List[any],valueof:Callable=ValOf)->List[List[any]]:

    """
    "this algorithm deconvert the partition of the converted jobs into a new parition of the original jobs
    >>> deconvertJobs([(1,1),(2,2),(3,3),(4,4)],[[(3, 3.75), (-1, 2.5)],[(4, 5.0), (-1, 2.5)]],5,2,[(1, 1), (2, 2)])
    [[(3, 3), (1, 1)], [(4, 4), (2, 2)]]
    """
    # >>> deconvertJobs([[124000,54768,89766,78900,101436,52422,17642],[34000,115256,43124,1000,23048,200102,65432]], 500000,500)
    [[124000,54768,89765,78900,101436,52422,17642],[34000,115256,43124,107,23047,200101,65432]]
    #deconvertPartition=[[]]*len(partition)
    deconvertPartition = [[] for _ in partition]
    numberOfSmallJobsPerM=[0]*len(partition)
    numberOfMachines=len(partition)
    # for i in range(numberOfMachines):
    #     numberOfSmallJobsPerM.append(0)
    numberOfSmallJobs=0 
    index=0   
    for machine in partition:
        machine = sorted(machine, key = valueof)
        for i,job in machine:
            if ValOf(job)>L/lambda_star:
                results = [t[1] for t in originalJobs if t[0] == i]
                deconvertPartition[index].append((i,results[0])) 
            else:
                #print(numberOfSmallJobsPerM[index])
                numberOfSmallJobsPerM[index]+=1  
                numberOfSmallJobs+=1        
        index+=1        
    curSmallJob=0  
    SJpartition=[[]]* numberOfMachines  
    smallSumForMachines=[0]*numberOfMachines         
    for machine in range(numberOfMachines):
        while smallSumForMachines[machine]<=(numberOfSmallJobsPerM[machine]-2)*(L/lambda_star):
            smallSumForMachines[machine]+=valueof(SmallJobs[curSmallJob])
            SJpartition[machine].append(SmallJobs[curSmallJob])
            deconvertPartition[machine].append(SmallJobs[curSmallJob])
            curSmallJob+=1

    for machine in range(numberOfMachines):
        while curSmallJob<numberOfSmallJobs:
            if smallSumForMachines[machine]<=((numberOfSmallJobsPerM[machine]-1)*(L/lambda_star)):
                smallSumForMachines[machine]+=valueof(SmallJobs[curSmallJob])
                SJpartition[machine].append(SmallJobs[curSmallJob])
                deconvertPartition[machine].append(SmallJobs[curSmallJob])
                curSmallJob+=1
            else:
                break    
   # print(deconvertPartition)
    return deconvertPartition


if __name__ == "__main__": 
    import doctest
    print(doctest.testmod()) 
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
    #list(range(10))
    import time
    for i in range(5,16):
        start = time.perf_counter()
        print(mainAlgorithm(BinsKeepingContents(3),list(range(1,i)),0.1, lambda x:x**2,ValOf))
        finish = time.perf_counter()
        print(f'Finished in {round(finish-start,2)} second(s)')