import numpy as np
from GPy.kern import RBF
from GPy.models import GPRegression
from matplotlib import pyplot as plt
from scipy.spatial.distance import cdist

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
        self.model = GPRegression(lecs, observable,self.kernel)

        

    def optimize(self, num_restarts=1):
        """Optimize the model."""
        
        #Something worng, model doesn't always converge
        self.model.optimize_restarts(num_restarts=num_restarts, messages=True)
        
    def rescale(inMatrix):
        """Rescales the input parameters that Gpy handles,
           so that they are in the interval [-1,1] #Remove 16xnr 
        """
       
        def rescale(colum):
            """Rescales the input parameters that Gpy handles,
            so that they are in the interval [-1,1] #Remove 16xnr 
            """
        
            translation = -(colum.max()+colum.min())/2
            new_array = colum + translation  #translation all the values
            scale = new_array.max()
            if scale == 0: # All values are 0 
                return new_array
            new_array =  new_array/scale #scale all the values
        
            return new_array
            
        return np.apply_along_axis( rescale, axis=0, arr=inMatrix) 
    
    def plot(self):
        """Plot the GP-model"""
        """Plot limits only for 1D-case"""
        print(self.model)
        self.model.plot()
        plt.show()


    """A measure of how great the model's error is compared to validation points
    Currently uses the average relative error
    """
    def get_model_error(self, Xvalid, Yvalid):
        (Ymodel, _) = self.model.predict(Xvalid)
        #Sum of a numpy array returns another array, we use the first (and only) element
        return (sum(abs((Ymodel-Yvalid)/Yvalid))/np.shape(Ymodel)[0])[0]


    def plot_modelerror(self, Xvalid, Xlearn, Yvalid):
        """ Creates a plot showing the vallidated error """
        alldists = cdist(Xvalid, Xlearn, 'euclidean')
        mindists = np.min(alldists, axis=1)
        (Ymodel, _) = self.model.predict(Xvalid)
        plt.figure(1)
        plt.plot(mindists, abs(Ymodel-Yvalid), '.')
        plt.xlabel('Distance to closest training point')
        plt.ylabel('Vallidated error')
        plt.axis([0, 1.1*max(mindists), 0, 1.1*max(abs(Ymodel-Yvalid))])
        #TODO: decide between fig1 and fig2
        plt.figure(2)
        plt.plot(mindists, abs((Ymodel-Yvalid)/Yvalid), '.')
        plt.xlabel('Distance to closest training point')
        plt.ylabel('Vallidated relative error')
        plt.axis([0, 1.1*max(mindists), 0, 1.1*max(abs((Ymodel-Yvalid)/Yvalid))])
        #TODO: fix x-scale
        plt.show()
        
        # plot the model of training data with the model of walidation data 
    def plot_model(self, Xvalid, Xlearn, Yvalid):
        (Ymodel, _) = self.model.predict(Xlearn)
        plt.figure(3)
        plt.plot(Xlearn, Ymodel, 'bo')
        plt.plot(Xvalid, Yvalid, 'rx')
        plt.show()
        
