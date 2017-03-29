#!/usr/bin/python
"""This module contains a basic python wrapper class for nsopt i python and
some related functions."""
import ctypes as c
import os
import sys
import numpy as np

def redirect_stdout():
    """Function that is called is the _init__ of PythonNsopt and is used to
    redirect most of the output of nsopt to /dev/null
    """
    #print "Redirecting stdout for nsopt"
    sys.stdout.flush() # <--- important when redirecting to files
    newstdout = os.dup(1)
    devnull = os.open(os.devnull, os.O_WRONLY)
    os.dup2(devnull, 1)
    os.close(devnull)
    sys.stdout = os.fdopen(newstdout, 'w')

class PythonNsopt(object):
    """PythonNsopt is a python class for representing and using nsopt in python.

    The current version of PythonNsopt is very basic and can only handel a
    specific case of .ini files and only return one observable.

    Attributes:
        path_libnsopt: is a path to libnsopt.so compiled library
        path_inifiles: is path to folder with .ini files for nsopt
        redirect: If the program should redirect and supress some of the
           output of nsopt. Default is true
    """

    def __init__(self, path_libnsopt, folder_inifiles, ini_string="", redirect=True, energy=None):
        """For more information on way the statup and configuration is done this
        way. See examplefile pyif.py by Boris"""

        # Load the library. Without RTLD_GLOBAL I get errors later when nsopt tries to use mkl-stuff
        if redirect:
            redirect_stdout()

        # Change directory to inifiles so they load properly
        old_dir = os.getcwd()
        path_inifiles = os.path.dirname(__file__) + folder_inifiles
        os.chdir(path_inifiles)

        self.nsopt = c.CDLL(path_libnsopt, c.RTLD_GLOBAL)
        self.ininow = c.c_int(2147483647)

        self.nsopt.program_startup_()
        # Read nsopt ini file
        self.nsopt.chp_ini_read_file(self.nsopt.cfast_ini_get(), b".",
                                     b"ns-input.ini", self.ininow)
        if ini_string != "":
            for line in ini_string.split('\n'):
                self.nsopt.chp_ini_read_line(self.nsopt.cfast_ini_get(), b".",
                                         line, self.ininow)
        if energy:
            self.nsopt.chp_ini_read_line(self.nsopt.cfast_ini_get(), b".",
                                         b"Elist=1 " + str(energy), self.ininow)

        self.nsopt.program_initialization_()

        self.res_nr = c.c_int(0) # Will hold number of residuals
        self.par_nr = c.c_int(0) # Will hold number of parameters that are optimized.
        self.par_extra_nr = c.c_int(0) # Number of extra parameters

        # Get the number of residuals from the program
        self.nsopt.get_nresiduals_(c.byref(self.res_nr))
        # Get the number of parameters
        self.nsopt.pounders_param_get_nr_(c.byref(self.par_nr))
        # Get the number of extra paraemters
        self.nsopt.get_par_extra_nr_.restype = c.c_int
        self.par_extra_nr = c.c_int(self.nsopt.get_par_extra_nr_())

        # residual_list is a derived fortran type so I can not use it directly in python.
        # That is why I created the global variable residual_list so that I have some space to use.
        # res will contain all needed information about the residuals (observables)
        self.res = self.nsopt.residual_mp_residual_list_
        self.nsopt.residual_mp_allocate_residual_list_type_(c.byref(self.res_nr),
                                                            c.byref(self.par_extra_nr),
                                                            self.res)

        self.tmp = c.c_double(0) # Temporary variable for getting data from nsopt
        # for giving parametervalues to nsopt
        self.par_vec_t = c.c_double * self.par_nr.value

        # Change back to old dir
        os.chdir(old_dir)

    def add_command(self, command):
        self.nsopt.chp_ini_read_line(self.nsopt.cfast_ini_get(), b".",
                                         command, self.ininow)
        
    def calculate_observable(self, par_vec):
        """Uses nsopt to do a calculation and returns the observable"""
        par_vec_c = self.par_vec_t(*par_vec)
        self.nsopt.calc_chi_squared_master_(par_vec_c, self.res,
                                            c.byref(self.par_nr))

        residuals = [0] * self.res_nr.value

        for i in range(self.res_nr.value):
            self.nsopt.residual_mp_get_residual_list_theo_val_(self.res,
                                                               c.byref(c.c_int(i + 1)),
                                                               c.byref(self.tmp))
            residuals[i] = self.tmp.value

        return np.array(residuals)

    def calculate_observable_par_matrix(self, par_matrix):
        """Uses nsopt to do a calculation for each set of parameters i par_matrix.

        Args:
            par_matrix: Matrix in shape (n_smaples,n_prameters)

        Returns:
            A column vector containing calculated observables for each sample
        """
        par_matrix = np.array(par_matrix) # Make sure par_matrix is an numpy array
        n_sampels = par_matrix.shape[0]
        values = [[] for i in range(n_sampels)]

        for i in range(n_sampels):
            values[i] = self.calculate_observable(par_matrix[i, :])

        return np.array(values)

    def terminate(self):
        """Does some cleanup of the program"""
        self.nsopt.residual_mp_deallocate_residual_list_type_(self.res)
        self.nsopt.program_termination_()
