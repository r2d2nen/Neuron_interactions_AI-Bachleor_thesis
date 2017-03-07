import numpy as np
from GPy.kern import RBF, Exponential, Matern32, Matern52
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
    
    def set_gp_kernel(self, kernel=DEFAULTS['kernel'], in_dim=DEFAULTS['input_dim'],
            variance=DEFAULTS['variance'], lengthscale=DEFAULTS['lengthscale'], multi_dim=False):
        """Sets the kernel of this Gaussfit"""
        if kernel == 'RBF':
            self.kernel = RBF(input_dim=in_dim, variance=variance, lengthscale=lengthscale,
                    ARD=multi_dim)
        elif kernel == 'Exponential':
            self.kernel = Exponential(input_dim=in_dim, variance=variance, lengthscale=lengthscale,
                    ARD=multi_dim)
        elif kernel == 'Matern32':
            self.kernel = Matern32(input_dim=in_dim, variance=variance, lengthscale=lengthscale,
                    ARD=multi_dim)
        elif kernel == 'Matern52':
            self.kernel = Matern52(input_dim=in_dim, variance=variance, lengthscale=lengthscale,
                    ARD=multi_dim)
        else:
            print 'Kernel not recognized or not implemented'
        
        
    def populate_gp_model(self, observable, lecs, energy=None, rescale=False):
        """Creates a model based on given data and kernel.
        
        Args:
        observable - numpy array with observable. (1 row for each observable from each lec sample)
        lecs - numpy array with lec parameters fit should be done with regard to (lec 1 coloum 1 and so on, sample 1 on row 1 and so on)
        energy - energy values 
        """
        # Add row with energies to parameters for fit (c for col if that is that is the right way)
        if energy is not None:
            lecs = np.r_(lecs, energy)
        if rescale:
            (lecs, observable) = self.rescale(lecs, observable)
        lecs.transpose()

        observable.transpose()
        self.model = GPRegression(lecs, observable, self.kernel)

    def optimize(self, num_restarts=1):
        """Optimize the model."""
        
        #Something worng, model doesn't always converge
        self.model.optimize_restarts(num_restarts=num_restarts, messages=True)
        print self.model
        
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
            self.scale[self.scale <= 1e-10] = 1
        outlecs = inlecs / self.scale[None,:16]
        outobs = inobs / self.scale[16]
        
        return (outlecs, outobs)

    def calculate_valid(self, Xvalid):
        """Calculates model prediction in validation points"""
        if self.scale is not None:
            Xvalid = (Xvalid-self.translate[None,:16]) / self.scale[None,:16]
            (Ymodel, Variance) = self.model.predict(Xvalid)
            Ymodel = Ymodel*self.scale[16] + self.translate[16]
            Variance = Variance*self.scale[16]*self.scale[16]
            return (Ymodel, Variance)
        else:
            return self.model.predict(Xvalid)

    def plot(self):
        """Plot the GP-model.
        Plot limits only for 1D-case.
        """
        print(self.model)
        self.model.plot()
        plt.show()

    def tags_to_title(self, train_tags, val_tags):
        """Create plot title from tags."""
        title = '_'.join(train_tags)
        title += '_' + '_'.join(val_tags)
        return title
        
    def save_fig_to_file(self, filename):
        """Saves the last specified global figure to file with filename
        File path specified by self.file_path.
        """
        plt.savefig(self.save_path + filename)


    def get_model_error(self, Ymodel, Yvalid):
        """A measure of how great the model's error is compared to validation points
        Currently uses the average relative error
        """
        #Sum of a numpy array returns another array, we use the first (and only) element
        return (sum(abs((Ymodel-Yvalid)/Yvalid))/np.shape(Ymodel)[0])[0]



    def plot_predicted_actual(self, Ymodel, Yvalid, Variance, train_tags, val_tags):
        """Plots the predicted values vs the actual values, adds a straight line and 2sigma error bars."""
        sigma = np.sqrt(Variance)
        plt.figure(1)
        plt.plot(Yvalid, Ymodel, '.')
        plt.errorbar(Yvalid, Ymodel, yerr=2*sigma, fmt='none')
        plt.plot([max(Yvalid), min(Yvalid)], [max(Yvalid), min(Yvalid)], '-')

        plt.xlabel('Simulated value [mb]')
        plt.ylabel('Emulated value [mb]')

        # Do we want to save to file?
        if self.save_fig:
            self.save_fig_to_file(self.tags_to_title(train_tags, val_tags) + "_predicted_actual.png")
        plt.show()
        



    def get_sigma_intervals(self, Ymodel, Yvalid, Variance):
        """Returns the fraction of errors within 1, 2, and 3 sigma."""
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

    def plot_modelerror(self, Xvalid, Xlearn, Ymodel, Yvalid, train_tags, val_tags):
        """ Creates a plot showing the vallidated error """
        alldists = cdist(Xvalid, Xlearn, 'euclidean')
        mindists = np.min(alldists, axis=1)
        plt.figure(1)
        plt.plot(mindists, Ymodel-Yvalid, '.')
        plt.xlabel('Distance to closest training point')
        plt.ylabel('Vallidated error [mb]')
        plt.axis([0, 1.1*max(mindists),  1.1*min(Ymodel-Yvalid), 1.1*max(Ymodel-Yvalid)])

        #Do we want to save val error to file?
        if self.save_fig:
            self.save_fig_to_file(self.tags_to_title(train_tags, val_tags) + "_val_error.png")
        #TODO: decide between fig1 and fig2
        plt.figure(2)
        plt.plot(mindists, (Ymodel-Yvalid)/Yvalid, '.')
        plt.xlabel('Distance to closest training point')
        plt.ylabel('Vallidated relative error')
        plt.axis([0, 1.1*max(mindists), 1.1*min((Ymodel-Yvalid)/Yvalid), 1.1*max((Ymodel-Yvalid)/Yvalid)])
        #TODO: fix x-scale

        #Do we want to save val error to file?
        if self.save_fig:
            self.save_fig_to_file(self.tags_to_title(train_tags, val_tags) + "_val_rel_error.png")
        plt.show()
        
    def plot_model(self, Xvalid, Ymodel, Yvalid):
        """Plot the model of training data with the model of walidation data."""
        plt.figure(3)
        plt.plot(Xvalid, Ymodel, 'bo')
        plt.plot(Xvalid, Yvalid, 'rx')
        plt.show()
        
