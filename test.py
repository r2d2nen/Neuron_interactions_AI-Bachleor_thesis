import sys
from parameters import Parameters
from nsoptcaller import NsoptCaller
from gaussfit import Gaussfit
from datamanager import Datamanager
from memory_profiler import profile
import numpy as np


#### BE CERTAIN TO SET THE TAGS AND WHICH LEC GENERATING METHOD YOU WANT TO USE!

#Do we want to generate new samples? And if so, how many? SET TAGS 
generate_data = False
process_data = True
rescale_data = False
save_fig = True
save_path = '/net/data1/ml2017/Test_tikz/'

# set True to save generated GPy model hyperparameters to file
save_params = False
params_save_path = '/net/data1/ml2017/gpyparams/xxxxxx.npy'

# set True to load GPy model hyperparameters from file
load_params = False
params_load_path = '/net/data1/ml2017/gpyparams/xxxxxx.npy'

# Generation parameters. Set these to generate different data
samples = 1000
lec_lhs = '1dof'   # Set 'lhs', 'gaussian', 'random_uniform', '1dof'
lec_index = '0' #With 1dof, which lec should we change integer 0 to 15, if not 1dof use empty string
interval = 1 # 0 to 1, percentage of total interval
lec_center = 'center_of_interval' # None --> N2LOsim500_290 optimum, or add your own vector with center
energy = 50

LEC_LENGTH = 16

#GPy parameters
kernel = 'RBF' #'RBF', 'Exponential', 'Matern32', 'Matern52'
lengthscale = 1.
multi_dim = False #Use multi-dimensional (16) lengthscale

# ONLY CHANGE training/validation and 'D_center_' to whatever your lec_center is and who you are
generate_tags = ['sgt' + str(energy), 'training' + str(samples),
                 'D_center_' + str(int(interval*100)) + '%_' + str(lec_lhs) + str(lec_index) + '_lecs' + '_' + kernel]


# Which tags to read from database i we process data? Set these manually
validation_tags = ['sgt50', 'validation1000', 'D_center_50%_lhs_lecs']

training_tags = ['sgt50', 'training500', 'D_center_100%_lhs_lecs']

# Set up necessary classes)
param = Parameters(1, samples, center_lecs=lec_center)
nsopt = NsoptCaller()
gauss = Gaussfit()
dm = Datamanager(echo=False)
gauss.save_fig = save_fig
gauss.save_path = save_path

@profile
def get_observable(lecs):
    """Wrapper function to measure time with memory profiler."""
    return nsopt.get_nsopt_observable(lecs)

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

# Sample generation, add to database. Do we want to generate and are the tags not used before?
# TODO(DANIEL): Add question if used really wants to add data to tags already used

if generate_data and dm.num_matches(generate_tags) <= 0:
    continue_generate = True
elif generate_data and dm.num_matches(generate_tags) > 0:
    answer = raw_input('Matching data for your tags already exist, add new data as well? (y for yes): ')
    if answer == 'y':
        continue_generate = True
else:
    continue_generate = False

if continue_generate:
    param.nbr_of_samples = samples
    if lec_lhs == 'lhs':
        print('lhs')
        lecs = param.create_lhs_lecs()
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
    observables = get_observable(lecs)
    
    for i in xrange(samples):
        dm.insert(tags=generate_tags, observable=observables[i][0], energy=energy, LECs=lecs[i])

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

    # Set up Gaussfit stuff and plot our model error
    gauss.set_gp_kernel(kernel=kernel, in_dim=LEC_LENGTH, lengthscale=lengthscale,
            multi_dim=multi_dim)

    if load_params:
        gauss.load_model_parameters(train_obs, train_lecs, params_load_path)
    else:
        train_gp_model(train_obs, train_lecs)

    if save_params:
        gauss.save_model_parameters(params_save_path)

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

    mod_obs, mod_var = calculate_valid(val_lecs)
            
    gauss.plot_predicted_actual(mod_obs, val_obs, mod_var,
                                training_tags, validation_tags)
    if save_fig:
        gauss.generate_and_save_tikz(mod_obs, val_obs, mod_var,
                                training_tags, validation_tags)
    
    print gauss.get_sigma_intervals(mod_obs, val_obs, mod_var)
    gauss.plot_modelerror(val_lecs, train_lecs, mod_obs, val_obs,
                          training_tags, validation_tags)
    print('Model error: ' + str(gauss.get_model_error(mod_obs, val_obs)))

