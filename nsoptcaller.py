from resources import python_nsopt
import numpy as np
import os
from matplotlib import pyplot as plt
import sys
import ConfigParser
import StringIO
import time
from multiprocessing import Process, Manager, cpu_count


# Init files and path to nsopt
PATH_LIBNSOPT = b'/net/home/andeks/software/nsopt/nucleon-scattering/libs/libnsopt.so.1.8.78.ml'
PATH_INIFILES = b'/'

class NsoptCaller:
    '''
    Rewriting this as a class

    The idea is that we use separate files for the physical problems, working something like:
    Generate data (with this class) -> Save data -> Use Gaussfit to fit GP -> analyze ....
    //Martin
    '''

    def __init__(self):
        '''Defining class variables'''
        self.energies = None
        self.observable = None

    def read_ini(self, args):
        """Reads .ini-file line by line and determines input arguments."""
        
        # Read and store the desiered lines
        txt_set = open('resources/set_parameters.ini', 'r')
        txt=""
        for line in txt_set:
            if 'evaluate_xsec' in line: break # Takes me to the line containg "evaluate_exsec" 
        
        for line in txt_set:
            if 'evaluate_ncsm' in line: break # Saves the line until "evaluate_ncsm"
            txt += line
        
        # Replace the content of evaluate_exsec.ini with the desired lines.
        txt_xsec = open('resources/evaluate_xsec.ini', 'w')
        txt_xsec.write(txt)
        txt_xsec.close()
        
        
        # Read and store the desiered lines
        txt_set = open('resources/set_parameters.ini', 'r')
        txt=""
        for line in txt_set:
            if 'evaluate_ncsm' in line: break # Takes me to the line containg "evaluate_ncsm" 
        
        for line in txt_set:
            txt += line
        
        # Replace the content of evaluate_xsec.ini with the desired lines.
        txt_ncsm = open('resources/evaluate_ncsm.ini', 'w')
        txt_ncsm.write(txt)
        txt_ncsm.close()

        config = StringIO.StringIO()
        config.write(open('resources/set_parameters.ini').read())
        config.seek(0, os.SEEK_SET)
    
        cp = ConfigParser.ConfigParser()
        cp.readfp(config)
    
        observable = cp.get('evaluate_xsec','observable')

        # List of input energies
        Elist = None

        # tries to read Elist
        try:
            Elist = cp.get('evaluate_xsec','Elist')
            Elist = np.fromstring(Elist,sep=" ")
            Elist = Elist[1:]
        except ConfigParser.NoOptionError:
            print "No Elist entry"

        # tries to read Emin, Emax, Esteps
        if Elist is None:
            try:
                Emin = cp.getfloat('evaluate_xsec','Emin')
                Emax = cp.getfloat('evaluate_xsec','Emax')
                Esteps = cp.getint('evaluate_xsec','Esteps')
            except ConfigParser.NoOptionError:
                print "No entries for Emin, Emax or Esteps"

        if args.nsopt:
            if observable == "SGT":
                if Elist is not None:
                    X = Elist
                    X = X.reshape(len(Elist),1)
                else:
                    X = np.linspace(Emin,Emax,Esteps)
                    X = X.reshape(1, Esteps)
                    #print "X from Emin, Emax, Esteps"
        else:
            X = np.random.uniform(-3.,3.,(20,1))
        
        self.energies = X
        return X

    def nsopt_calculation(self, energy, lecs, number, observable_list):
        """Target function for multiprocessing for calculating nsopt observables for different energies. """
        evaluate = 'include evaluate_xsec.ini'
        nsopt = python_nsopt.PythonNsopt(PATH_LIBNSOPT, PATH_INIFILES, ini_string=evaluate, energy=energy)
        observable_list[number] = nsopt.calculate_observable(lecs)
        nsopt.terminate()

    def remove_finished_process(self, process_list):
        """Check if any processes has stopped, if it has. Delete them from our list"""
        for idx, process in enumerate(process_list):
            if not process.is_alive():
                process.join()
                del process_list[idx]
            
    
   
    def get_nsopt_observable(self, energies, LECM=None):    
        """
        Takes a matrix of LECs LECM and calls nsopt to calculate the observable. Each row in LECM is a
        set of LECs. Returns nsopt_observable where each row corresponds to a different set of LECs.
Energy is a vector with energies associated with each sample
        Reads a set of default LEC values if no LECM is given.
        """
        
        # sets default LECM
        if LECM is None:
            pot = 'N2LOsim'
            lam = 500
            cut = 290

            # remove some LECs from analysis
            removed_LECs = (14,17,18,19,20,21,22,23,24,25)

            # reads 1 set of default LEC-values from text file
            LECM = np.loadtxt(b'./resources/%s-%d-%d.LEC_values.txt' %(pot,lam,cut) )
            LECM = np.delete(LECM,removed_LECs)

        # makes LECM 2D array if it is 1D array to work with code
        if len(LECM.shape) == 1:
            LECM = LECM.reshape(1,-1)

        # evaluate = 'include evaluate_ncsm.ini'

       
        # Set up manager for distributing a observable list between processes.
        manager = Manager()
        observables = manager.list(range(len(LECM)))
        process_list = []
        MAX_PROCESSES = cpu_count() - 1 if  cpu_count() > 1 else 1 
        
         # calls nsopt for each set of LECs in LECM
        for i in range(len(LECM)):
            process = Process(target=self.nsopt_calculation, args=(energies[i], LECM[i,:], i, observables))
            process.start()
            process_list.append(process)

            # Wait for a process spot to be empty
            while len(process_list) >= MAX_PROCESSES:
                self.remove_finished_process(process_list)
                time.sleep(0.5)

        # Empty process list
        while process_list:
            self.remove_finished_process(process_list)
            time.sleep(1)

        print(observables)

        tmp_obs = np.asarray(observables)
        trimmed_obs = np.zeros(len(tmp_obs))
        for row in xrange(len(tmp_obs)):
        
            trimmed_obs[row] = np.trim_zeros(tmp_obs[row,:])

           

        self.observable = trimmed_obs
        return self.observable
