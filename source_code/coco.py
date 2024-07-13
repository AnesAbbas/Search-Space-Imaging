#!/usr/bin/env python
"""A short and simple example experiment with restarts.

The code is fully functional but mainly emphasises on readability.
Hence produces only rudimentary progress messages and does not provide
batch distribution or timing prints, as `example_experiment2.py` does.

To apply the code to a different solver, `fmin` must be re-assigned or
re-defined accordingly. For example, using `cma.fmin` instead of
`scipy.optimize.fmin` can be done like::

>>> import cma  # doctest:+SKIP
>>> def fmin(fun, x0):
...     return cma.fmin(fun, x0, 2, {'verbose':-9})

"""
from __future__ import division, print_function
import cocoex, cocopp  # experimentation and post-processing modules
import scipy.optimize  # to define the solver to be benchmarked
from numpy.random import rand  # for randomised restarts
import os, webbrowser  # to show post-processed results in the browser

import pso
import mario_short

import time
from multiprocessing import Pool

def optimize(x):
    # ### input
    suite_name = "bbob"
    output_folder = x
    # fmin = scipy.optimize.fmin
    budget_multiplier = 1  # increase to 10, 100, ...

    ### prepare
    suite = cocoex.Suite(suite_name, "", "")
    observer = cocoex.Observer(suite_name, "result_folder: " + output_folder)
    # minimal_print = cocoex.utilities.MiniPrint()


    fun = -1
    dim = -1
    print ("Starting: ",x)
    startTime = time.time()
    ### go
    for problem in suite:  # this loop will take several minutes or longer

        problem.observe_with(observer)  # generates the data for cocopp post-processing

        # if problem.dimension <> 2 or problem.id_instance <> 1:
        #     continue
        # if problem.id_function <> 1:
        #     continue
        # if problem.dimension not in [2,3,5] :
        #     continue
        if problem.dimension == 40 :
            continue

        # # apply restarts while neither the problem is solved nor the budget is exhausted
        # while (problem.evaluations < problem.dimension * budget_multiplier and not problem.final_target_hit):
        #     fmin(problem, x0, disp=False)  # here we assume that `fmin` evaluates the final/returned solution
  
        # print(x," name",problem.name)
        # print("function_id",problem.id_function)
        # # print("dimension",problem.dimension)
        # print("lower_bounds",problem.lower_bounds)
        # print("upper_bounds",problem.upper_bounds)
        # print("initial_solution",problem.initial_solution)
        # # print("evaluations_constraints",problem.evaluations_constraints)
        # print("evaluations",problem.evaluations)
        # print("final_target_hit",problem.final_target_hit)
        # # print("index",problem.index)
        # if problem.id_instance == 1:
        #     print ("Starting ",x,"-",problem.name, time.asctime( time.localtime(time.time())) )

        # if fun <> problem.id_function:
        #     fun = problem.id_function
        #     print(x,"- ",problem.name)
        # print (".")

        if problem.id_function == 1 and problem.id_instance == 1:
            sTime = time.time()

        pso.run(10000*problem.dimension,50,problem,x)

        if problem.id_function == 24 and problem.id_instance == 80:
            eTime = time.time() 
            workTime =  eTime - sTime
            f = open("Timings/"+x+".txt", "a+")
            f.write(x +"- D" + str(problem.dimension) + "Done: " + str(workTime) + "\n")
            f.close()
 
        # if dim <> problem.dimension:
        #     dim = problem.dimension
        #     print(x,"- D",problem.dimension , "Done" )
        
         # return 1
        # mario_short.t()
        # minimal_print(problem, final=problem.index == len(suite) - 1)
 
    endTime = time.time()
    workTime =  endTime - startTime
    print (x," is Done. Time elapsed:" + str(workTime) + " seconds")

    f = open("Timings/summary.txt", "a+")
    f.write(x + " is Done. Time elapsed:" + str(workTime) + " seconds" +"\n")
    f.close()
    # ### post-process data
    # cocopp.main(observer.result_folder)  # re-run folders look 

    # webbrowser.open("file://" + os.ge tcwd() + "/ppdata/index.html")
    # mario_short.t()
    return 1

if __name__ == '__main__':
    for i in [9]:
        startTime = time.time()
        #create a process Pool with 4 processes
        pool = Pool(processes=i)
        #map doWork to availble Pool processes
        results = pool.map(optimize, ("PSO","iSN","iLN","iFW","iCN","mSN","mLN","mFW","mCN"))
        # results = pool.map(optimize, ("PSO","iSN","iLN","iFW","iCN","iLN5","iFW5","iCN5","iLNp5","iFWp5","mSN","mLN","mFW","mCN","mSN8","mLN8","mFW8","mCN8","mSN4","mLN4","mFW4","mCN4"))
        # results = pool.map(optimize, ("iSN"))
        #mark the end time
        endTime = time.time()
        #calculate the total time it took to complete the work
        workTime =  endTime - startTime
        #print results
        print ("Done. Took " + str(workTime) + " seconds to complete")
        mario_short.t()