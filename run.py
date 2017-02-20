import StringIO
import argparse
import numpy as np

#import project files
from gaussfit import Gaussfit
from ml2017 import ml2017
from datamanager import Datamanager

def main():
    """Controls the program flow determined by user input"""

    # Parses arguments supplied by the user. 
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbosity", action="store_true", help="Show data output")
    
    # Add a group of arguments that can't coexist
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-f", "--function", action="store", help="Use specified function for GP")
    group.add_argument("-n", "--nsopt", action="store_true", help="Use nsopt calculation for GP")
    group.add_argument("-l", "--load", action="store", help="Use stored data for GP") #Add tag handling
    args = parser.parse_args()

    # Initialize project class objects
    nsopt = ml2017()
    gauss = Gaussfit()
    dm = Datamanager()

    # Read input arguments to get input vector
    X = nsopt.read_ini(args)

    # Do we want to genereate new nsopt values or use specified function.
    if args.nsopt:
        Y = nsopt.get_nsopt_observable()
        Y = np.trim_zeros(Y)
        Y = Y.reshape(len(Y),1)
    else:
        Y = np.sin(X) + np.random.randn(20,1)*0.03

    # Set up GP-processes and plot output after optimization.
    gauss.set_gp_kernel()
    gauss.populate_gp_model(X, Y)
    gauss.optimize()
    gauss.plot()



if __name__ == '__main__':
    main()
