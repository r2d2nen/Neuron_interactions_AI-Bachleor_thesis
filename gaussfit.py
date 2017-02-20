import numpy as np
from GPy.kern import RBF
from GPy.models import GPRegression
from matplotlib import pyplot as plt

#Default values for the GP
DEFAULTS = {'kernel': 'RBF', 'input_dim': 1, 'variance': 1., 'lengthscale': 1.}

class Gaussfit:

    def __init__(self):
        '''Initialize a gaussfit object '''
        self.kernel = None
        self.model = None
    
    def set_gp_kernel(self, kernel=DEFAULTS['kernel'], in_dim=DEFAULTS['input_dim'], variance=DEFAULTS['variance'], lengthscale=DEFAULTS['lengthscale']):
        '''Sets the kernel of this Gaussfit'''
        '''Need to manually add the different kernels'''
        if kernel == 'RBF':
            self.kernel = RBF(input_dim=in_dim, variance=variance, lengthscale=lengthscale)
        else:
            print 'Kernel not recognized'
    

    def populate_gp_model(self, X, Y):
        '''Creates a model based on given data and kernel''' 
        self.model = GPRegression(X, Y, self.kernel)

    def optimize(self):
        '''Optimize the model. TODO: add verbose'''
        '''Something worng, model doesn't always converge'''
        self.model.optimize(messages=True)
    
    def plot(self):
        '''Plot the GP-model'''
        '''Plot limits only for 1D-case'''
        self.model.plot()
        plt.show()
