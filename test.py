import sys
from parameters import Parameters
from nsoptcaller import NsoptCaller
from gaussfit import Gaussfit
from datamanager import Datamanager
from memory_profiler import profile
import numpy as np
import pickle

#### BE CERTAIN TO SET THE TAGS AND WHICH LEC GENERATING METHOD YOU WANT TO USE!

#Do we want to generate new samples? And if so, how many? SET TAGS 
generate_data = True
process_data = False
rescale_data = False

save_fig = False     
save_params = False # set True to save generated GPy model hyperparameters,
                    # which training tags and model are used to
                    # file. Saves objecs in .pickle with with pickle module.
load_params = False  # set True to load GPy model from file 
save_fig_path = '/net/data1/ml2017/presentation/'
params_save_path = '/net/data1/ml2017/gpyparams/E_curve_gpy/Matern52_E_curve_training_500_lhs_sgt1_150_multidim.pickle'
params_load_path = '/net/data1/ml2017/gpyparams/energy1_150_multidim/RBF_training_2500_100lhs_sgt1_150_multidim.pickle'

# Generation parameters. Set these to generate different data
samples = 500     # Number of datapoints
lec_sampling = 'lhs'  # Set 'lhs', 'gaussian', 'random_uniform', '1dof'
lec_index = ''   # With 1dof, which lec should we change integer 0 to 15, if not 1dof use empty string
interval = 1     # 0 to 1, percentage of total interval
lec_center = 'center_of_interval' # None --> N2LOsim500_290 optimum, or add your own vector with center

#THIS ONLY WORKS FOR LHS LECS AS OF NOW. (STASR, STOP)
# If start and stop is the same. Training is done wiht only lecs as parameters and not anything else
energy = (1, 50)

LEC_LENGTH = 16

#GPy parameters
kernel = 'Matern52'
lengthscale = 1.
multi_dim = True #Use multi-dimensional lengthscale

# ONLY CHANGE training/validation and 'D_center_' to whatever your lec_center is and who you are
generate_tags = ['sgt' + str(energy[0]) + '-' +  str(energy[1]), 'training' + str(samples),
                 'testing' + str(lec_sampling) + str(lec_index)]


# Which tags to read from database i we process data? Set these manually
# training tags will be read from file if load option is used

validation_tags = ['sgt50', 'validation500', 'mem_center_100%_lhs_lecs']

if load_params:
    with open(params_load_path, 'r') as f:
        tagsidx = 2
        training_tags = pickle.load(f)[tagsidx]
else:
    training_tags = ['sgt50', 'validation1100', 'mem_center_100%_lhs_lecs']

#------------------------------------------------------------------------------------------
# Actual code

# Training dimension, do we want to train on energy or only lecs?
# This is for generation
parameter_dim = LEC_LENGTH
energy_as_param = False
if energy[1] != energy[0]:
    parameter_dim += 1
    energy_as_param = True

# Set up necessary classes)
param = Parameters(interval, samples, center_lecs=lec_center)
nsopt = NsoptCaller()
gauss = Gaussfit()
dm = Datamanager(echo=False)
gauss.save_fig = save_fig
gauss.save_path = save_fig_path

@profile
def get_observable(energies, lecs):
    """Wrapper function to measure time with memory profiler."""
    return nsopt.get_nsopt_observable(energies,LECM=lecs)

@profile
def train_gp_model(train_obs, train_lecs):
    """Populate and optimize GP model."""
    gauss.populate_gp_model(train_obs, train_lecs, rescale=rescale_data)
    gauss.optimize()
    
@profile
def calculate_valid(val_lecs):
    """Wrapper function to measure time with memory profiler."""
    mod_obs, mod_var = gauss.calculate_valid(val_lecs)
    return mod_obs, mod_var

# Check if data tags is already in database
if generate_data and dm.num_matches(generate_tags) <= 0:
    continue_generate = True
elif generate_data and dm.num_matches(generate_tags) > 0:
    answer = raw_input('Matching data for your tags already exist, add new data as well? (y for yes): ')
    if answer == 'y':
        continue_generate = True
else:
    continue_generate = False

# Generate 
if continue_generate:
    param.nbr_of_samples = samples
    
    if lec_sampling == 'lhs':
        print('lhs')
        if energy_as_param:     # Do we want to have energies samples as well?
            lecs = param.create_lhs_lecs(energy_interval=energy)
            energies = lecs[:,-1]
            lecs = lecs[:,0:-1]
        else:
            energies = np.linspace(energy[0], energy[0], samples) # Need list of energies anyway for nsoptcaller
            lecs = param.create_lhs_lecs()
    elif lec_sampling == 'gaussian':
        print('gaussian')
        lecs = param.create_gaussian_lecs()
    elif lec_sampling == 'random_uniform':
        print('random_uniform')
        lecs = param.create_random_uniform_lecs()
    elif lec_sampling == '1dof':
        print('1dof lec index: ' + str(lec_index))
        lecs = param.create_lecs_1dof()
    print(generate_tags)

    # Call nsopt and get the calculated values. Time consuming now since it uses subprocess
    # method for all calls for now.
    observables = get_observable(energies, lecs)

    for i in xrange(samples):
        print(observables[i])
        dm.insert(tags=generate_tags, observable=observables[i], energy=energies[i], LECs=lecs[i])


# Data processing
if process_data:
    if dm.num_matches(training_tags) <= 0 or dm.num_matches(validation_tags) <= 0:
        sys.exit('Check your tags. No matched found in database.')
    
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

  # Check if we have different energies, if we do we train with them
  # Same for validation,
  # Warning if they are not the same.
    train_energy_as_param = False
    train_parameter_dim = LEC_LENGTH
    if not np.all(train_energy==train_energy[0], axis = 0)[0]:
        train_parameter_dim = LEC_LENGTH + 1
        train_energy_as_param = True
        train_lecs = np.hstack((train_lecs, train_energy))

    val_energy_as_param = False
    val_parameter_dim = LEC_LENGTH
    if not np.all(val_energy==val_energy[0], axis = 0)[0]:
        val_parameter_dim = LEC_LENGTH + 1
        val_energy_as_param = True
        val_lecs = np.hstack((val_lecs, val_energy))

    # Warning for energy not used in one of val or train
    if train_energy_as_param != val_energy_as_param:
        answer = raw_input('Training data energy or validation data energy is constant. This is bad: ')
        
    # Set up our kernel
    gauss.set_gp_kernel(kernel=kernel, in_dim=train_parameter_dim, lengthscale=lengthscale,
            multi_dim=multi_dim)

    # Have we already trained a GP that we load or do we train a new one_
    if load_params:
        gauss.load_model_parameters(train_obs, train_lecs, params_load_path)
    else:
        train_gp_model(train_obs, train_lecs)

    if save_params:
        gauss.save_model_parameters(params_save_path, training_tags, kernel, train_parameter_dim,
                                    lengthscale, multi_dim, rescale_data)

    # Get prediction from GP
    mod_obs, mod_var = calculate_valid(val_lecs)


    # Fix plot stuff and stuff
    
    gauss.plot_energy_curve(mod_obs,val_obs, mod_var, val_energy)
    gauss.plot_predicted_actual(mod_obs, val_obs, mod_var,
                                 training_tags, validation_tags)
    if save_fig:
         gauss.generate_and_save_tikz(mod_obs, val_obs, mod_var,
                                 training_tags, validation_tags)
    
    print gauss.get_sigma_intervals(mod_obs, val_obs, mod_var)
    gauss.plot_modelerror(val_lecs, train_lecs, mod_obs, val_obs,
                           training_tags, validation_tags)
    print('Model error: ' + str(gauss.get_model_error(mod_obs, val_obs)))

