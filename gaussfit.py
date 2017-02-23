import numpy as np
from GPy.kern import RBF
from GPy.models import GPRegression
from matplotlib import pyplot as plt

#Default values for the GP
DEFAULTS = {'kernel': 'RBF', 'input_dim': 1, 'variance': 1., 'lengthscale': 1.}

class Gaussfit:
    """Handles GPR of input data. """
    def __init__(self):
        """Initialize a gaussfit object."""
        self.kernel = None
        self.model = None
    
    def set_gp_kernel(self, kernel=DEFAULTS['kernel'], in_dim=DEFAULTS['input_dim'], variance=DEFAULTS['variance'], lengthscale=DEFAULTS['lengthscale']):
        """Sets the kernel of this Gaussfit"""
        """Need to manually add the different kernels"""
        if kernel == 'RBF':
            self.kernel = RBF(input_dim=in_dim, variance=variance, lengthscale=lengthscale)
        else:
            print 'Kernel not recognized'
    

    def populate_gp_model(self, observable, lecs, energy=None):
        """Creates a model based on given data and kernel.
        
        Args:
        observable - numpy array with observable. (1 row for each observable from each lec sample)
        lecs - numpy array with lec parameters fit should be done with regard to (lec 1 coloum 1 and so on, sample 1 on row 1 and so on)
        energy - energy values 
        """
        # Add row with energies to parameters for fit (c for col if that is that is the right way)
        if energy is not None:
        lecs = np.r_(lecs, energy)
        lecs.transpose()

        observable.transpose()
        self.model = GPRregression(input_dim=lecs.shape()[0],observable, lecs ,self.kernel)

        

    def optimize(self, num_restarts=1):
        """Optimize the model."""
        
        #Something worng, model doesn't always converge
        self.model.optimize_restarts(num_restarts=num_restarts, messages=True)
    
    def plot(self):
        """Plot the GP-model"""
        """Plot limits only for 1D-case"""
        print(self.model)
        self.model.plot()
        plt.show()
