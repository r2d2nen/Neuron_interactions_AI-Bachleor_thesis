import sys
from parameters import Parameters
from nsoptcaller import NsoptCaller
from gaussfit import Gaussfit
from datamanager import Datamanager
from memory_profiler import profile
import numpy as np
import pickle
from matplotlib import pyplot as plt
from matplotlib2tikz import save as tikz_save
from fix_tikz import EditText
from scipy.spatial.distance import cdist
from math import sqrt
from matplotlib import style


def calculate_valid(val_lecs):
    """Wrapper function to measure time with memory profiler."""
    mod_obs, mod_var = gauss.calculate_valid(val_lecs)
    return mod_obs, mod_var



params_load_dir = '/net/data1/ml2017/gpyparams/E_curve_gpy/'
save_fig_dir = '/net/data1/ml2017/presentation/energy_curve/'


samples = 3000     # Number of datapoints
lec_sampling = 'lhs'  # Set 'lhs', 'gaussian', 'random_uniform', '1dof'
lec_index = ''   # With 1dof, which lec should we change integer 0 to 15, if not 1dof use empty string
interval = 1     # 0 to 1, percentage of total interval
lec_center = 'center_of_interval' # None --> N2LOsim500_290 optimum, or add your own vector with center

#THIS ONLY WORKS FOR LHS LECS AS OF NOW. (STASR, STOP)
# If start and stop is the same. Training is done wiht only lecs as parameters and not anything else
energy = (1, 150)

LEC_LENGTH = 16



# Set up necessary classes)
param = Parameters(interval, samples, center_lecs=lec_center)
nsopt = NsoptCaller()
gauss = Gaussfit()
dm = Datamanager(echo=False)
#gauss.save_fig = False
#gauss.save_path = save_fig_path

validation_tags = ['validation300', 'sgt1-150', 'single_lec_E_curve25/50lhs']

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

kernels = ['RBF', 'Matern52']

RBF_train_obs = []
RBF_train_energy = []
RBF_train_lecs = []
RBF_model_error = []
RBF_mod_obs = []

Matern52_train_obs = []
Matern52_train_energy = []
Matern52_train_lecs = []
Matern52_model_error = []
Matern52_mod_obs = []

samples = range(250, 3001, 250)

for kernel in kernels:
    for sample in samples:
        params_load_path = params_load_dir + kernel + '_E_curve_training_' + str(sample) + '_lhs_sgt1_150_multidim.pickle'

        with open(params_load_path, 'r') as f:
            tagsidx = 2
            training_tags = pickle.load(f)[tagsidx]

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
        train_lecs = np.hstack((train_lecs, train_energy))

        gauss.load_model_parameters(train_obs, train_lecs, params_load_path)

        mod_obs, mod_var = calculate_valid(val_lecs)

        model_error = gauss.get_model_error(mod_obs, val_obs)

        if kernel == 'RBF':

            RBF_train_obs.append(train_obs)
            RBF_train_energy.append(train_energy)
            RBF_train_lecs.append(train_lecs)
            RBF_model_error.append(model_error)
            RBF_mod_obs.append(mod_obs)

        if kernel == 'Matern52':
            Matern52_train_obs.append(train_obs)
            Matern52_train_energy.append(train_energy)
            Matern52_train_lecs.append(train_lecs)
            Matern52_model_error.append(model_error)
            Matern52_mod_obs.append(mod_obs)



file_name = 'model_error'


fig = plt.figure()

#style.use('fivethirthyeight')

plt.plot(samples, RBF_model_error, label='RBF')
plt.plot(samples, Matern52_model_error, label='Matern52')
plt.legend(loc='upper left')

 

plt.xlabel('Training samples')   #****Edit****
plt.ylabel('Model error')   #****Edit****
plt.grid(True)
plt.show()




#from matplotlib2tikz import save as tikz_save
        
#The folowing saves the file to folder as well as adding 3 rows. 
#The "clip mode=individual" was a bit tricky to add so this is the ugly way to solve it.
#tikz_save(save_fig_dir + file_name, 
 #################################          figureheight = '\\textwidth*0.8,\nclip mode=individual',
#           figurewidth = '\\textwidth*0.8')
        
# #Last fix of tikz.
# from fix_tikz import EditText
# edit = EditText()
# #Making transformable to PNG
# edit.fix_file(save_fig_dir + file_name, '% This file was created by matplotlib2tikz v0.6.3.', '\documentclass{standalone}\n\usepackage{tikz}\n\usepackage{pgfplots}\n\usepackage{siunitx}\n\n\\begin{document}')
        
# edit.fix_file(save_path + fileName, '\end{document}', '')
# edit.fix_file(save_path + fileName, '\end{tikzpicture}', '\end{tikzpicture}\n\end{document}')




            

# def tryint(s):
#     try:
#         return int(s)
#     except:
#         return s
     
# def alphanum_key(s):
#     """ Turn a string into a list of string and number chunks.
#         "z23a" -> ["z", 23, "a"]
#     """
#     return [ tryint(c) for c in re.split('([0-9]+)', s) ]

# def sort_nicely(l):
#     """ Sort the given list in the way that humans expect.
#     """
#     l.sort(key=alphanum_key)


# def generate_and_save_tikz(self, fileName, save_path):
#     fig = plt.figure()
#     style.use('seaborn-bright')
        
#         #****************Insert the ploting*********************
#     # Training 100-3000
#     kernels = ['RBF', 'Exponential', 'Matern32', 'Matern52']
#     rbf_train_memory = []
#     exp_train_memory = []
#     mat32_train_memory = []
#     mat52_train_memory = []
#     train_memory = [rbf_train_memory, exp_train_memory, mat32_train_memory, mat52_train_memory]
    
#     rbf_val_memory = []
#     exp_val_memory = []
#     mat32_val_memory = []
#     mat52_val_memory = []
#     val_memory = [rbf_val_memory, exp_val_memory, mat32_val_memory, mat52_val_memory]
#     style.use('fivethirtyeight')
#     for index, kernel in enumerate(kernels):
#         filenames = [f for f in listdir(destpath) if isfile(join(destpath, f)) and kernel in f]
#         sort_nicely(filenames)
#         print(filenames)
    
#         val = 0
#         train_samples = []
#         val_samples = []
#         for file in filenames:
#             val += 100
#             with open(join(destpath, file), 'r') as inF:
#                 times = []
#                 memories = []
#                 for line in inF:
#                     if 'MEM' in line:
#                         entries = line.split()
#                         times.append(float(entries[2]))
#                         memories.append(float(entries[1]))
#                     if 'train' in line:
#                         entries = line.split()
#                         train_start = float(entries[-3])
#                         train_stop = float(entries[-1])
#                     if 'val' in line:
#                         entries = line.split()
#                         val_start = float(entries[-3])
#                         val_stop = float(entries[-1])
#                 train_max = 0
#                 val_max = 0
#                 for i, mem in enumerate(memories):
#                     if times[i] >= train_start and times[i] <= train_stop:
#                         train_max = max(train_max, mem)
#                     if times[i] >= val_start and times[i] <= val_stop:
#                         val_max = max(val_max, mem)
#                 train_samples.append(val)
#                 val_samples.append(val)
#                 train_memory[index].append(train_max)
#                 val_memory[index].append(val_max)
#     print(kernel)
#     #plt.figure(3)
#     #plt.plot(train_samples, train_memory[index], label=kernel)
#     #plt.figure(4)
#     plt.plot(val_samples, val_memory[index], label=kernel)
#     #plt.figure(3)
#     plt.legend(loc='upper left')
#     plt.xlabel('Data points')
#     plt.ylabel('Time [s]')
#     #plt.grid(True)
#     #plt.figure(4)
#     #plt.legend(loc='upper left')
#     #plt.xlabel('Data points')
#     #plt.ylabel('Time [s]')
#     #plt.grid(True)
#     #plt.show()
        
        
#     plt.xlabel('X-label')   #****Edit****
#     plt.ylabel('Y-label')   #****Edit****
#     plt.grid(True)

#     from matplotlib2tikz import save as tikz_save
        
#     #The folowing saves the file to folder as well as adding 3 rows. 
#     #The "clip mode=individual" was a bit tricky to add so this is the ugly way to solve it.
#     tikz_save(save_path + '/' + fileName, 
#     figureheight = '\\textwidth*0.8,\nclip mode=individual',
#     figurewidth = '\\textwidth*0.8')
        
#     #Last fix of tikz.
#     from fix_tikz import EditText
#     edit = EditText()
#     #Making transformable to PNG
#     edit.fix_file(save_path + '/' + fileName, '% This file was created by matplotlib2tikz v0.6.3.', '\documentclass{standalone}\n\usepackage{tikz}\n\usepackage{pgfplots}\n\usepackage{siunitx}\n\n\\begin{document}')
        
#     edit.fix_file(save_path + '/' + fileName, '\end{document}', '')
#     edit.fix_file(save_path + '/' + fileName, '\end{tikzpicture}', '\end{tikzpicture}\n\end{document}')
