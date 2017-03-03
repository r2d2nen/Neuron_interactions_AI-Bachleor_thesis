from parameters import Parameters
from nsoptcaller import NsoptCaller
from gaussfit import Gaussfit
from datamanager import Datamanager
import numpy as np


#### BE CERTAIN TO SET THE TAGS AND WHICH LEC GENERATING METHOD YOU WANT TO USE!

#Do we want to generate new samples? And if so, how many? SET TAGS 
generate_data = True
process_data = False
rescale_data = False

# Generation parameters
samples = 1000
lec_lhs = 'random_uniform'   # Set 'lhs', 'gaussian', 'random_uniform', '1dof'
lec_index = '' #With 1dof, which lec should we change integer 0 to 15, if not 1dof use empty string
interval = 1 # 0 to 1, percentage of total interval
lec_center = 'center_of_interval' # None --> N2LOsim500_290 optimum, or add your own vector with center
energy = 50
LEC_LENGTH = 16

generate_tags = ['sgt' + str(energy), 'training' + str(samples),
                 'D_center_' + str(interval*100) + '%_' + str(lec_lhs) + str(lec_index) + '_lecs']


# Which tags to read from database i we process data?
training_tags = ['sgt50', 'training1000', 'D_center_100%_lhs_lecs']
validation_tags = ['sgt50', 'validation1000', 'D_center_100%_gaussian_lecs']


# Set up necessary classes)
param = Parameters(1, samples, center_lecs=lec_center)
nsopt = NsoptCaller()
gauss = Gaussfit()
dm = Datamanager(echo=False)



# Sample generation, add to database. Do we want to generate and are the tags not used before?
# TODO(DANIEL): Add question if used really wants to add data to tags already used
#for samples in xrange(200, 1600, 100):
    

if generate_data and dm.num_matches(generate_tags) <= 0:
    continue_generate = True
elif generate_data and dm.num_matches(generate_tags) > 0:
    answer = raw_input('Matching data for your tags already exist, add new data as well? (y for yes): ')
    if answer == 'y':
        continue_generate = True


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
    observables = nsopt.get_nsopt_observable(lecs)
    
    for i in xrange(samples):
        dm.insert(tags=generate_tags, observable=observables[i][0], energy=energy, LECs=lecs[i])
    
    #for row in dm.read(['test']):
        #print row.observable
        #print(param.create_monospaced_lecs())
        #print(param.create_lhs_lecs())
            
if process_data:
    #Set empty arrays with zeros for training and validation data
    train_obs = np.array([0])
    train_energy = np.array([0])
    train_lecs = np.array(np.zeros(LEC_LENGTH))

    #Read database data with the specified tags
    for row in dm.read(training_tags):
        train_obs = np.vstack((train_obs, row.observable))
        train_energy = np.vstack((train_energy, row.energy))
        train_lecs = np.vstack((train_lecs, row.LECs))

    if rescale_data:
        train_lecs = gauss.scale(train_lecs)
     
    # Clean up initialized zeros
    train_obs = np.delete(train_obs, 0, 0)
    train_energy = np.delete(train_energy, 0, 0)
    train_lecs = np.delete(train_lecs, 0, 0)

    # Set up Gaussfit stuff and plot our model error
    gauss.set_gp_kernel(in_dim=LEC_LENGTH)
    #train_lecs = gauss.rescale(train_lecs)
    gauss.populate_gp_model(train_obs, train_lecs)
    gauss.optimize()
    
    for sample in xrange(100, 200, 100):
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

        if rescale_data:
            val_lecs = gauss.rescale(val_lecs)
            
        gauss.plot_predicted_actual(val_lecs, val_obs)
        print gauss.get_sigma_intervals(val_lecs, val_obs)
        gauss.plot_modelerror(val_lecs, train_lecs, val_obs)
        print('Number of validation data: ' + str(sample))
        print('Model error: ' + str(gauss.get_model_error(val_lecs, val_obs)))

