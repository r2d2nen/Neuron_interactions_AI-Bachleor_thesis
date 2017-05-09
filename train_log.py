import sys
from parameters import Parameters
from nsoptcaller import NsoptCaller
from gaussfit import Gaussfit
from datamanager import Datamanager
from memory_profiler import profile
import numpy as np
import pickle

def train_gp_model(train_obs, train_lecs):
    """Populate and optimize GP model."""
    gauss.populate_gp_model(train_obs, train_lecs, rescale=rescale_data)
    gauss.optimize()

save_params = True
gauss = Gaussfit()
dm = Datamanager(echo=False)
kernels = ['RBF', 'Matern52']
samples = range(250, 3001, 250)

for kernel in kernels:
    for training_number in xrange(250, 3001, 250):

        print("Training kernel {} training_number {}".format(kernel, training_number))

        training_tags = ['sgt1-150', 'training' + str(training_number), 'E_curvelhs']
        params_save_path = '/net/data1/ml2017/gpyparams/E_curve_gpy_log/' + str(kernel) + '_E_curve_training_' + str(training_number) + '_lhs_sgt1_150_multidim_log.pickle'

        #Set empty arrays with zeros for training and validation data
        train_obs = np.array([0])
        train_energy = np.array([0])

        LEC_LENGTH = 16
        
        train_lecs = np.array(np.zeros(LEC_LENGTH))

        #Read database data with the specified tags
        for row in dm.read(training_tags):
            train_obs = np.vstack((train_obs, row.observable))
            train_energy = np.vstack((train_energy, row.energy))
            train_lecs = np.vstack((train_lecs, row.LECs))
    
        # Clean up initialized zeros
        train_obs = np.delete(train_obs, 0, 0)
        train_energy = np.delete(train_energy, 0, 0)
        train_lecs = np.delete(train_lecs, 0, 0)
        
        train_lecs = np.hstack((train_lecs, train_energy))

        train_obs = np.log(train_obs)

        train_parameter_dim = 17
        lengthscale = 1.0
        rescale_data = False
        multi_dim = True

        gauss.set_gp_kernel(kernel=kernel, in_dim=train_parameter_dim, lengthscale=lengthscale,
                            multi_dim=True)

        train_gp_model(train_obs, train_lecs)
        
        gauss.save_model_parameters(params_save_path, training_tags, kernel, train_parameter_dim,
                                    lengthscale, multi_dim, rescale_data)

