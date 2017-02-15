from resources import python_nsopt
import numpy as np
import os
from GPy.kern import RBF
from GPy.models import GPRegression
from matplotlib import pyplot as plt
import sys
import argparse

# Init files and path to nsopt
PATH_LIBNSOPT = b'/net/home/andeks/software/nsopt/nucleon-scattering/libs/libnsopt.so.1.8.78.ml'
PATH_INIFILES = b'/'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbosity", action="store_true", help="Show data output")
    group= parser.add_mutually_exclusive_group()
    group.add_argument("-f", "--function", action="store", help="Use specified function for GP")
    group.add_argument("-n", "--nsopt", action="store_true", help="Use nsopt calculation for GP")
    args = parser.parse_args()

    if args.nsopt:
        Y = get_nsopt_observable()
        Y = np.trim_zeros(Y)
        Y = Y.reshape(100,1)
        X = np.linspace(1., 290., 100)
        X = X.reshape(100,1)
    else:
        X = np.random.uniform(-3.,3.,(20,1))
        Y = np.sin(X) + np.random.randn(20,1)*0.03
        
    model = get_gp_model(X,Y)
    plot_gp(model)

def get_nsopt_observable():
    pot = 'N2LOsim'
    lam = 500
    cut = 290

    #remove some LECs from the analysis
    #e.g. *.cov.name - files for list
    removed_LECs = (14,17,18,19,20,21,22,23,24,25)

    #read covariance matrix of LECs
    cov = np.loadtxt(b'./resources/%s-%d-%d.cov.txt' %(pot,lam,cut) )
    cov = np.delete(cov,removed_LECs,0)
    cov = np.delete(cov,removed_LECs,1)

    #read LEC order
    LEC_name = np.loadtxt(b'./resources/%s-%d-%d.cov.name' %(pot,lam,cut) ,dtype='S12')
    LEC_name = np.delete(LEC_name,removed_LECs)
    #read LEC values
    LEC_value = np.loadtxt(b'./resources/%s-%d-%d.LEC_values.txt' %(pot,lam,cut) )
    LEC_value = np.delete(LEC_value,removed_LECs)

    LEC_sigma = np.sqrt(np.diag(cov))
    
    print
    print '%5s %25s %25s %25s' % ('no.','LEC','value','sigma')
    for i in range(len(LEC_name)):
        print '%5d %25s %25f %25f' %(i, LEC_name[i], LEC_value[i], LEC_sigma[i])
    
    par_vec = np.array(LEC_value)

    scale = 1.0
    print 'sigma scale = %10f' %(scale)
    cov = np.multiply(cov,scale*scale)
    nof_samples = 1

    X_samples = np.random.multivariate_normal(par_vec, cov, size=nof_samples)

    evaluate = 'include evaluate_xsec.ini'
    # evaluate = 'include evaluate_ncsm.ini'
    nsopt = python_nsopt.PythonNsopt(PATH_LIBNSOPT, PATH_INIFILES, ini_string=evaluate)
    nsopt_observables = nsopt.calculate_observable(X_samples[0,:])
    #print nsopt_observables

    nsopt.terminate()

    return nsopt_observables

def get_gp_model(X,Y):
    """Return a GPR-model of X,Y(X) with a RBF kernel."""
    kernel = RBF(input_dim=1., variance=1., lengthscale=1.)
    model = GPRegression(X, Y, kernel)
    return model

def plot_gp(model):
    """Plot the GP-model"""
    model.plot()
    model.optimize()
    model.plot()
    plt.show()

if __name__ == '__main__':
    main()
