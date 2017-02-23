from parameters import Parameters
from nsoptcaller import NsoptCaller
#from gaussfit import Gaussfit
from datamanager import Datamanager
import numpy as np

param = Parameters(0.1, 3)
nsopt = NsoptCaller()
#gauss = Gaussfit()
dm = Datamanager(echo=True)

lecs = param.create_lhs_lecs()

#nsopt.read_ini(None) #I think args is not used
nsopt.X = 50
observables = nsopt.get_nsopt_observable(lecs)

print '###Energy'
print nsopt.X
print '###Observables'
print observables
print '###LECs'
print lecs

#print(param.create_monospaced_lecs())
#print(param.create_lhs_lecs())



