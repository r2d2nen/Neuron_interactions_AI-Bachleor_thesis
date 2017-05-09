import sys
from parameters import Parameters
from nsoptcaller import NsoptCaller
from gaussfit import Gaussfit
from datamanager import Datamanager
from memory_profiler import profile
import numpy as np
import pickle

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import style
from matplotlib2tikz import save as tikz_save
from os import listdir
from os.path import isfile, join
from shutil import move, copyfile
from matplotlib import pyplot as plt
from matplotlib import style


# The kernels we have trained fro
kernels = ['RBF', 'Matern52']

gauss = Gaussfit()
dm = Datamanager(echo=False)

def calculate_valid(val_lecs):
    """Wrapper function to measure time with memory profiler."""
    mod_obs, mod_var = gauss.calculate_valid(val_lecs)
    return mod_obs, mod_var

LEC_LENGTH = 16
RBF_error = []
Matern52_error = []
samples = range(250, 3001, 250)

# Kernel loop
for kernel in kernels:
    for training_number in [250, 500, 2750, 3000]:
# no log
#--------------------------------------------------------------------------------
        params_load_path = '/net/data1/ml2017/gpyparams/E_curve_gpy_log/' + kernel + '_E_curve_training_' + str(training_number) + '_lhs_sgt1_150_multidim.pickle'

        with open(params_load_path, 'r') as f:
            tagsidx = 2
            training_tags = pickle.load(f)[tagsidx]



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

        train_lecs = np.hstack((train_lecs, train_energy))

        train_obs = np.log(train_obs)
        
        gauss.load_model_parameters(train_obs, train_lecs, params_load_path)

        #model_error = 0

# log
#        -------------------------------------------------------------------------------

        params_load_path = '/net/data1/ml2017/gpyparams/E_curve_gpy_log/' + kernel + '_E_curve_training_' + str(training_number) + '_lhs_sgt1_150_multidim_log.pickle'

        with open(params_load_path, 'r') as f:
            tagsidx = 2
            training_tags = pickle.load(f)[tagsidx]



        train_log_obs = np.array([0])
        train_log_energy = np.array([0])
        train_log_lecs = np.array(np.zeros(LEC_LENGTH))

        #Read database data with the specified tags
        for row in dm.read(training_tags):
            train_log_obs = np.vstack((train_log_obs, row.observable))
            train_log_energy = np.vstack((train_log_energy, row.energy))
            train_log_lecs = np.vstack((train_log_lecs, row.LECs))

        # Clean up initialized zeros
        train_log_obs = np.delete(train_log_obs, 0, 0)
        train_log_energy = np.delete(train_log_energy, 0, 0)
        train_log_lecs = np.delete(train_log_lecs, 0, 0)

        train_log_lecs = np.hstack((train_log_lecs, train_log_energy))

        train_log_obs = np.log(train_log_obs)
        
        gauss.load_model_parameters(train_log_obs, train_log_lecs, params_load_path)# Loop over all validation


#        -------------------------------------------------------------------------------
        for validation_number in xrange(1, 51):

            validation_tags = ['sgt1-150', 'validation300','single_lec_E_curve' + str(validation_number) + '/50lhs']

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

            val_lecs = np.hstack((val_lecs, val_energy))

# no log
#        -------------------------------------------------------------------------------
            
            val_obs = np.log(val_obs)

            mod_obs, mod_var = calculate_valid(val_lecs)

            #plt.figure(1)
            #plt.plot(val_energy, np.exp(mod_obs))
            #plt.plot(val_energy, np.exp(val_obs))
            #plt.show()

            model_error += gauss.get_model_error(mod_obs, val_obs)

# log
#        -------------------------------------------------------------------------------

            print('Completed ' + kernel + ' training ' + str(training_number) + ' validation ' + str(validation_number) + '/50')

        if kernel == 'RBF':
            RBF_error.append(model_error/50)

        if kernel == 'Matern52':
            Matern52_error.append(model_error/50)

print(RBF_error)
print(Matern52_error)

fig = plt.figure()
style.use('seaborn-bright')
plt.figure(1)


plt.plot(samples, RBF_error, label='RBF')
plt.plot(samples, Matern52_error, label='Matern52')
plt.legend(loc='upper left')
plt.xlabel('Number of sample points')   #****Edit****
plt.ylabel('Model error')   #****Edit****
plt.grid(True)
#plt.show()


fileName = 'energy_log_error.tex'
save_path = '/net/home/dakarlss/ml2017'

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
