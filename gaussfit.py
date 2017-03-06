import numpy as np
from GPy.kern import RBF
from GPy.models import GPRegression
from matplotlib import pyplot as plt
from scipy.spatial.distance import cdist
from math import sqrt

#Default values for the GP
DEFAULTS = {'kernel': 'RBF', 'input_dim': 1, 'variance': 1., 'lengthscale': 1.}

class Gaussfit:
    """Handles GPR of input data. """
    def __init__(self):
        """Initialize a gaussfit object."""
        self.kernel = None
        self.model = None
        self.scale = None
        self.translate = None
        self.save_fig = False
        self.save_path = None

    @property
    def save_fig(self):
        return self.save_fig

    @save_fig.setter
    def save_fig(self, save_fig):
        self.save_fig = save_fig

    @property
    def save_path(self):
        return self.save_path

    @save_path.setter
    def save_path(self, save_path):
        self.save_path = save_path
    
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
        
    def rescale(self, inlecs, inobs):
        """Rescales the input parameters that Gpy handles,
           so that they are in the interval [-1,1] #Remove 16xnr 
        """
        
        if self.translate is None:
            self.translate = np.append(np.mean(inlecs, axis=0), np.mean(inobs))
        
        inlecs = inlecs - self.translate[None,:16]
        inobs = inobs - self.translate[16]
        
        if self.scale is None:
            self.scale = np.append(np.amax(abs(inlecs), axis=0), max(abs(inobs)))
            self.scale[self.scale == 0] = 1
        outlecs = inlecs / self.scale[None,:16]
        outobs = inobs / self.scale[16]

        return (outlecs, outobs)
        '''def rescale(colum):
            """Rescales the input parameters that Gpy handles,
            so that they are in the interval [-1,1] #Remove 16xnr 
            """

            if self.translate is None:
                self.translate = np.mean(colum)
            colum = colum - self.translate
            
            if self.scale is None: #allows only for on value of scale for each gauss object
                self.scale = max(abs(colum))
            if self.scale == 0: # All values are 0 
                return colum
            new_array =  colum/self.scale #scale all the values
        
            return new_array
            
        return np.apply_along_axis(rescale, axis=0, arr=inMatrix)'''

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


    """
    Plots the predicted values vs the actual values, adds a straight line and 2sigma error bars
    """
    def plot_predicted_actual(self, Xvalid, Yvalid, training_tags=' ', validation_tags=' '):
        (Ymodel, Variance) = self.model.predict(Xvalid)
        sigma = np.sqrt(Variance)
        plt.figure(1)
        plt.plot(Yvalid, Ymodel, '.')
        plt.errorbar(Yvalid, Ymodel, yerr=2*sigma, fmt='none')
        plt.plot([max(Yvalid), min(Yvalid)], [max(Yvalid), min(Yvalid)], '-')
        plt.xlabel('Simulated value')
        plt.ylabel('Predicted value')
        title1 = ''.join(training_tags)
        title1 += ' | ' + ' '.join(validation_tags)
        plt.title(title1)
        if self.save_fig:
            plt.savefig(self.save_path + title1 + "_predicted_actual.png")
        plt.show()
        
    """
    Returns the fraction of errors within 1, 2, and 3 sigma 
    """
    def get_sigma_intervals(self, Xvalid, Yvalid):
        (Ymodel, Variance) = self.model.predict(Xvalid)
        sigma = np.sqrt(Variance)
        n = np.array([0, 0, 0])
        errors = abs(Yvalid - Ymodel)
        for i, e in enumerate(errors):
            if e <= sigma[i]:
                n[0] = n[0] + 1
            if e <= 2 * sigma[i]:
                n[1] = n[1] + 1
            if e <= 3 * sigma[i]:
                n[2] = n[2] + 1
        return n/float(np.shape(errors)[0])

    def plot_modelerror(self, Xvalid, Xlearn, Yvalid, training_tags=' ', validation_tags=' ' ):
        """ Creates a plot showing the vallidated error """
        alldists = cdist(Xvalid, Xlearn, 'euclidean')
        mindists = np.min(alldists, axis=1)
        (Ymodel, _) = self.model.predict(Xvalid)
        plt.figure(1)
        plt.plot(mindists, Ymodel-Yvalid, '.')
        plt.xlabel('Distance to closest training point')
        plt.ylabel('Vallidated error')
        plt.axis([0, 1.1*max(mindists),  1.1*min(Ymodel-Yvalid), 1.1*max(Ymodel-Yvalid)])
        title1 = ' '.join(training_tags)
        title1 += ' | ' + ' '.join(validation_tags)
        plt.title(title1)
        if self.save_fig:
            plt.savefig(self.save_path + title1 + "_val_error.png")
            
        #TODO: decide between fig1 and fig2
        plt.figure(2)
        plt.plot(mindists, (Ymodel-Yvalid)/Yvalid, '.')
        plt.xlabel('Distance to closest training point')
        plt.ylabel('Vallidated relative error')
        plt.axis([0, 1.1*max(mindists), 1.1*min((Ymodel-Yvalid)/Yvalid), 1.1*max((Ymodel-Yvalid)/Yvalid)])
        title2 = ' '.join(training_tags)
        title2 += ' | ' + ' '.join(validation_tags)
        plt.title(title2)
        #TODO: fix x-scale
        if self.save_fig:
            plt.savefig(self.save_path + title2 + "_val_rel_error.png")
        plt.show()
        
        # plot the model of training data with the model of walidation data 
    def plot_model(self, Xvalid, Xlearn, Yvalid):
        (Ymodel, _) = self.model.predict(Xlearn)
        plt.figure(3)
        plt.plot(Xlearn, Ymodel, 'bo')
        plt.plot(Xvalid, Yvalid, 'rx')
        plt.show()
        
