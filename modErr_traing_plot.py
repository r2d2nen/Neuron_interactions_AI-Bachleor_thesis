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
process_data = True
rescale_data = False

save_fig = False     


#THIS ONLY WORKS FOR LHS LECS AS OF NOW. (STASR, STOP)
# If start and stop is the same. Training is done wiht only lecs as parameters and not anything else
energy = (50, 50)

LEC_LENGTH = 16

#GPy parameters
lengthscale = 1.


impportantList = [ [ [ [] ] ] ] 
    
#---------------------------------------
 
    
save_params = False # set True to save generated GPy model hyperparameters,
                    # which training tags and model are used to
                    # file. Saves objecs in .pickle with with pickle module.
load_params = True  # set True to load GPy model from file 
params_save_path = '/net/data1/ml2017/gpyparams/E_curvelhs_Matern52_2500.pickle'
params_load_path = '/net/data1/ml2017/gpyparams/E_curvelhs_RBF3000.pickle'
    
multi_dim = True #Use multi-dimensional lengthscale   
    


# Which tags to read from database i we process data? Set these manually
# training tags will be read from file if load option is used

validation_tags = ['sgt50', 'validation1000', 'mem_center_100%_lhs_lecs']
    
    
    
kernels = ['RBF', 'Exponential', 'Matern32_', 'Matern52_']

        
for numberK, kernel in enumerate(kernels):
        
    #Remove after first go.
    if kernel is 'RBF':
        save_params = True
        load_params = False
    else:
        save_params = False
        load_params = True
        
    for numberT, times in enumerate['', '_1', '_2']:        
        
        for numberM, index in enumerate(xrange(250,3001,250)):


            if load_params:
                with open(params_load_path, 'r') as f:
                    tagsidx = 2
                    training_tags = pickle.load(f)[tagsidx]
            else:
                train_dat= 'training' + index
                training_tags = ['sgt50', 'mem_center_100%_lhs_lecs', training_dat ]
                
            params_save_path = '/net/data1/ml2017/gpyparams/E_curvelhs_'+ kernel + (str)index + times +'.pickle'
            params_load_path = '/net/data1/ml2017/gpyparams/E_curvelhs_'+ kernel + (str)index + times +'.pickle'
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

                print('Model error: ' + str(gauss.get_model_error(mod_obs, val_obs)))
        
                impportantList[numberK][numberT][numberM] = str(gauss.get_model_error(mod_obs, val_obs))
    
    
   
#------------------------------------------------
#plot this nicely and save
fileName = moddleError_trainingponts_median.tex
save_path = /net/data1/ml2017/mem_profiles/plots_thesis
generate_and_save_tikz()


def generate_and_save_tikz(self, fileName, save_path, importantList):
        fig = plt.figure()
        style.use('seaborn-bright')
        
        #****************Insert the ploting*********************
        meanValu = [[]]
        
        #RBF
        meanValu[0] =importantList[0][0][:] + importantList[0][1][:] + importantList[0][2][:]
        #Exponential
        meanValu[1] =importantList[1][0][:] + importantList[1][1][:] + importantList[1][2][:]
        #Matern32
        meanValu[2] =importantList[2][0][:] + importantList[2][1][:] + importantList[2][2][:]
        #Matern52
        meanValu[3] =importantList[3][0][:] + importantList[3][1][:] + importantList[3][2][:]
        xVal = range(250,3000,250)
        
        for i in range(0,3):
            plt.plot(Xval, meanValu[i])
        
        plt.xlabel('Training')   #****Edit****
        plt.ylabel('Number of training points')   #****Edit****
        plt.grid(True)

        from matplotlib2tikz import save as tikz_save
        
        #The folowing saves the file to folder as well as adding 3 rows. 
        #The "clip mode=individual" was a bit tricky to add so this is the ugly way to solve it.
        tikz_save(save_path + '/' + fileName, 
        figureheight = '\\textwidth*0.8,\nclip mode=individual',
        figurewidth = '\\textwidth*0.8')
        
        #Last fix of tikz.
        from fix_tikz import EditText
        edit = EditText()
        #Making transformable to PNG
        edit.fix_file(save_path + '/' + fileName, '% This file was created by matplotlib2tikz v0.6.3.', '\documentclass{standalone}\n\usepackage{tikz}\n\usepackage{pgfplots}\n\usepackage{siunitx}\n\n\\begin{document}')
        
        edit.fix_file(save_path + '/' + fileName, '\end{document}', '')
        edit.fix_file(save_path + '/' + fileName, '\end{tikzpicture}', '\end{tikzpicture}\n\end{document}')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

