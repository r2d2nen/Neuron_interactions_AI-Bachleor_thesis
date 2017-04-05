import sys
from parameters import Parameters
from nsoptcaller import NsoptCaller
from gaussfit import Gaussfit
from datamanager import Datamanager
#from memory_profiler import profile
import numpy as np
import pickle

# Generation parameters. Set these to generate different data
samples = 150
lec_lhs = 'lhs'   # Set 'lhs', 'gaussian', 'random_uniform', '1dof'
lec_index = '' #With 1dof, which lec should we change integer 0 to 15, if not 1dof use empty string
interval = 1 # 0 to 1, percentage of total interval
lec_center = 'center_of_interval' # None --> N2LOsim500_290 optimum, or add your own vector with center

#THIS ONLY WORKS FOR LHS LECS AS OF NOW. (START, STOP)
energy = (1, 150)

LEC_LENGTH = 16

#GPy parameters
kernel = 'Matern52'
lengthscale = 1.
multi_dim = True #Use multi-dimensional (16) 

generate_tags = ['sgt' + str(energy), 'validation1_' + str(samples),
                 'energy_curve' + str(int(interval*100)) + '%_' + str(lec_lhs) + str(lec_index) + '_lecs']



# Set up necessary classes)
param = Parameters(interval, samples, center_lecs=lec_center)
nsopt = NsoptCaller()
gauss = Gaussfit()
dm = Datamanager(echo=False)

if dm.num_matches(generate_tags) > 0:
    answer = raw_input('Matching data for your tags already exist, add new data as well? (y for yes): ')
    if answer == 'y':
        continue_generate = True

def get_observable(energies, lecs):
    """Wrapper function to measure time with memory profiler."""
    return nsopt.get_nsopt_observable(energies,LECM=lecs)

param.nbr_of_samples = samples
if lec_lhs == 'lhs':
    print('lhs')
    lecs = param.create_lhs_lecs(energy_interval=energy)
    energies = lecs[:,-1]
    lecs = lecs[:,0:-1]
        

    # Make this so we get all energies in interval with
    energies = np.linspace(1, 150, num=samples)
    chosen_row = lecs[0,:]
    lecs[:] = chosen_row
elif lec_lhs == 'gaussian':
    print('gaussian')
    lecs = param.create_gaussian_lecs()
elif lec_lhs == 'random_uniform':
    print('random_uniform')
    lecs = param.create_random_uniform_lecs()
elif lec_lhs == '1dof':
    print('1dof lec index: ' + str(lec_index))
    lecs = param.create_lecs_1dof()
print(generate_tags)
observables = get_observable(energies, lecs)

for i in xrange(samples):
    print(observables[i])
    dm.insert(tags=generate_tags, observable=observables[i], energy=energies[i], LECs=lecs[i])
print('hj')
