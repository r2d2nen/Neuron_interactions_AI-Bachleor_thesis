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

    #Add tag handling. Supports multiple arg seperated by space.
    group.add_argument("-l", "--load", nargs='+', action='append', help="Use stored data for GP") 
    args = parser.parse_args()

    # Initialize project class objects
    nsopt = ml2017()
    gauss = Gaussfit()
    dm = Datamanager()

    # Read input arguments to get input vector
    X = nsopt.read_ini(args)
    
    # Load all data with the right tags
    if args.load != None:
        data = dm.read(args.load[0])


    # Do we want to genereate new nsopt values or use specified function.
    if args.nsopt:
        Y = nsopt.get_nsopt_observable()
        Y = np.trim_zeros(Y)
        Y = Y.reshape(len(Y),1)
    else:
        Y = np.sin(X) + np.random.randn(20,1)*0.03

    # Set up GP-processes and plot output after optimization.
    gauss.set_gp_kernel()

    #TODO(rikard) Is this what I was sopposed to do?
    if args.load != None:
        gauss.populate_gp_model(data) #TODO(rikard) Check data format. Need to refine data?
    else:
        gauss.populate_gp_model(X, Y)
    
    gauss.optimize()
    gauss.plot()



if __name__ == '__main__':
    main()
