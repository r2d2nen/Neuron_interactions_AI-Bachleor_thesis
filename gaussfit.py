import numpy as np
from GPy.kern import RBF
from GPy.models import GPRegression
from matplotlib import pyplot as plt

#Default values for the GP
DEFAULTS = {'input_dim': 1, 'variance': 1., 'lengthscale': 1.}

def get_gp_model(X, Y, in_dim=None, variance=None, lengthscale=None):
    """Return a GPR-model of X,Y(X) with a RBF kernel."""
    if not in_dim:
        in_dim = DEFAULTS['input_dim']
    if not variance:
        variance= DEFAULTS['variance']
    if not lengthscale:
        lengthscale = DEFAULTS['lengthscale']

    kernel = RBF(input_dim=in_dim, variance=variance, lengthscale=lengthscale)
    model = GPRegression(X, Y, kernel)
    return model

def plot_gp(model):
    """Plot the GP-model"""
    model.plot()
    model.optimize()
    model.plot()
    plt.show()
