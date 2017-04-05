import sys
from parameters import Parameters
from nsoptcaller import NsoptCaller
from gaussfit import Gaussfit
from datamanager import Datamanager
#from memory_profiler import profile
import numpy as np
import pickle

# Load gpy params
loadpath = '/net/data1/ml2017/gpyparams/energy1_150_multidim/Matern52_training_500_100lhs_sgt1_150_multidim.pickle'
gauss = Gaussfit()



