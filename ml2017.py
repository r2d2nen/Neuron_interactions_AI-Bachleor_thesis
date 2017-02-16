from resources import python_nsopt
import ConfigParser
import StringIO
import numpy as np
import os
from matplotlib import pyplot as plt
import sys
import argparse

#import project files
from gaussfit import Gaussfit

# Init files and path to nsopt
PATH_LIBNSOPT = b'/net/home/andeks/software/nsopt/nucleon-scattering/libs/libnsopt.so.1.8.78.ml'
PATH_INIFILES = b'/'

class ml2017:
    '''
    Rewriting this as a class

    The idea is that we use separate files for the physical problems, working something like:
    Generate data (with this class) -> Save data -> Use Gaussfit to fit GP -> analyze ....
    //Martin
    '''

    def __init__(self):
        '''Definiera klassvariabler'''
        pass

    def read_ini(self, args):
        # read .ini file
        config = StringIO.StringIO()
        config.write('[dummysection]\n')
        config.write(open('resources/evaluate_xsec.ini').read())
        config.seek(0, os.SEEK_SET)
    
        cp = ConfigParser.ConfigParser()
        cp.readfp(config)
    
        observable = cp.get('dummysection','observable')
    
        Elist = None
        
        try:
            Elist = cp.get('dummysection','Elist')
            print type(Elist)
            print Elist
            Elist = np.fromstring(Elist,sep=" ")
            print type(Elist)
            print Elist
            Elist = Elist[1:]
            print Elist
        except ConfigParser.NoOptionError:
            print "No Elist entry"
    
        if Elist is None:
            try:
                Emin = cp.getfloat('dummysection','Emin')
                Emax = cp.getfloat('dummysection','Emax')
                Esteps = cp.getint('dummysection','Esteps')
            except ConfigParser.NoOptionError:
                print "No entries for Emin, Emax or Esteps"
    
        if args.nsopt:
            if observable == "SGT":
                if Elist is not None:
                    X = Elist
                    X = X.reshape(len(Elist),1)
                    print X
                    print X.shape
                    print "X from Elist"
                else:
                    X = np.linspace(Emin,Emax,Esteps)
                    X = X.reshape(Esteps, 1)
                    print "X from Emin, Emax, Esteps"
        else:
            X = np.random.uniform(-3.,3.,(20,1))
    
        return X
    
    def main(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-v", "--verbosity", action="store_true", help="Show data output")
        group= parser.add_mutually_exclusive_group()
        group.add_argument("-f", "--function", action="store", help="Use specified function for GP")
        group.add_argument("-n", "--nsopt", action="store_true", help="Use nsopt calculation for GP")
        args = parser.parse_args()
    
        X = self.read_ini(args)
        
        if args.nsopt:
            Y = self.get_nsopt_observable()
            Y = np.trim_zeros(Y)
            Y = Y.reshape(len(Y),1)
        else:
            Y = np.sin(X) + np.random.randn(20,1)*0.03
        
        self.Gauss = Gaussfit()
        self.Gauss.set_gp_kernel()
        self.Gauss.populate_gp_model(X, Y)
        self.Gauss.optimize()
        self.Gauss.plot()
    
    def get_nsopt_observable(self):
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
    
if __name__ == '__main__':
    ml = ml2017()
    ml.main()
