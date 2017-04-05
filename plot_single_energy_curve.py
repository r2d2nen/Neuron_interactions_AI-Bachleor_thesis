import sys
from parameters import Parameters
from nsoptcaller import NsoptCaller
from gaussfit import Gaussfit
from datamanager import Datamanager
#from memory_profiler import profile
import numpy as np
import pickle

param = Parameters(interval, samples, center_lecs=lec_center)
nsopt = NsoptCaller()
gauss = Gaussfit()
dm = Datamanager(echo=False)
gauss.save_fig = save_fig
gauss.save_path = save_path

if dm.num_matches(training_tags) <= 0 or dm.num_matches(validation_tags) <= 0:
        sys.exit('Check your tags. No matched found in database.')
else:
    #Set empty arrays with zeros for training and validation data
    train_obs = np.array([0])
    train_energy = np.array([0])
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

    # Set up Gaussfit stuff and plot our model error
    gauss.set_gp_kernel(kernel=kernel, in_dim=LEC_LENGTH, lengthscale=lengthscale,
            multi_dim=multi_dim)

    if load_params:
        gauss.load_model_parameters(train_obs, train_lecs, params_load_path)
    else:
        # Add energy to lecs for training
        train_lecs = np.hstack((train_lecs, train_energy))
        train_gp_model(train_obs, train_lecs)

    if save_params:
        gauss.save_model_parameters(params_save_path, training_tags, kernel, LEC_LENGTH,
                                    lengthscale, multi_dim, rescale_data)

    val_obs = np.array([0])
    val_energy = np.array([0])
    val_lecs = np.array(np.zeros(LEC_LENGTH))
    #validation_tags[1] = 'validation' + str(sample)
    for row in dm.read(validation_tags):
        val_obs = np.vstack((val_obs, row.observable))
        val_energy = np.vstack((val_energy, row.energy))
        val_lecs = np.vstack((val_lecs, row.LECs))
                
    val_obs = np.delete(val_obs, 0, 0)
    val_energy = np.delete(val_energy, 0, 0)
    val_lecs = np.delete(val_lecs, 0,0)

    # Add energy to lecs for validation
    val_lecs = np.hstack((val_lecs, val_energy))
