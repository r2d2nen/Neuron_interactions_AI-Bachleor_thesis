import StringIO
import argparse
import numpy as np

#import project files
from gaussfit import Gaussfit
from ml2017 import ml2017
from datamanager import Datamanager

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbosity", action="store_true", help="Show data output")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-f", "--function", action="store", help="Use specified function for GP")
    group.add_argument("-n", "--nsopt", action="store_true", help="Use nsopt calculation for GP")
    group.add_argument("-l", "--load", action="store_true", help="Use stored data for GP") #Add tag handling
    args = parser.parse_args()

    '''Project class objects'''
    nsopt = ml2017()
    gauss = Gaussfit()
    dm = Datamanager()

    X = nsopt.read_ini(args)
    
    if args.nsopt:
        Y = nsopt.get_nsopt_observable()
        Y = np.trim_zeros(Y)
        Y = Y.reshape(len(Y),1)
    else:
        Y = np.sin(X) + np.random.randn(20,1)*0.03
    
    gauss.set_gp_kernel()
    gauss.populate_gp_model(X, Y)
    gauss.optimize()
    gauss.plot()



if __name__ == '__main__':
    main()
