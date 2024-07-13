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

# ### post-process data
# cocopp.main(observer.result_folder)  # re-run folders look
# cocopp.main('-o ppdata exdata\FW-001 exdata\FW-002')  # re-run folders look
# cocopp.main('-o ppdata5  exdata\PSO exdata\iSN exdata\iLN exdata\iFW exdata\iCN \
# exdata\iLN5 exdata\iFW5 exdata\iCN5 \
# exdata\iLNp5 exdata\iFWp5 \
# exdata\mSN8 exdata\mLN8 exdata\mFW8 exdata\mCN8 \
# exdata\mSN4 exdata\mLN4 exdata\mFW4 exdata\mCN4 \
# exdata\mSN exdata\mLN exdata\mFW exdata\mCN')
cocopp.main('-o ppdata exdata\PSO exdata\iSN exdata\iLN exdata\iFW exdata\mSN exdata\mLN exdata\mFW')  # re-run folders look 
# # cocopp.main('exdata\scipy-optimize-1 exdata\scipy-optimize-2')  # re-run folders look like "...-001" etc
# webbrowser.open("file://" + os.getcwd() + "/ppdata/index.html")
webbrowser.open("file://" + os.getcwd() + "/ppdata/index.html")
mario_short.t()