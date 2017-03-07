import numpy as np
import pyDOE as pydoe
from scipy.spatial.distance import pdist
from scipy.optimize import minimize

class Parameters():
    """Handles input and generation of LECs.
    """


    # PARAMETER OVERHAUL
    # Bring back functionality for center_lecs as center of interval
    # Can we move outside of physical boundarys for lecs?
    # 
    # Make Parameters great again!
    #
    
    def __init__(self, interval_width, nbr_of_samples, center_lecs=None, nbr_of_points_1d = 3,
                 maxfun=2000000, maxiter=1000, disp=True):
        """Set up parameter volume from supplied intervals.
        
        Args:
        Center_lecs - numpy array with center points which we would like to sample lecs around
        Interval_width - total interval width around the center point in parts (0 to 1 where 0.10 means 10 percent)
        nbr_of_samples - number of data points we want to generate in the volume.
        nbr_of_points_1d - number of sample points to be generated for each lec dimension
        (used by create_monospaced_lecs)
        maxfun - number of function evaluations used by optimizer
        maxiter - number of iterations in optimizer
        disp - prints convergence results in optimizer if true
        """
        
        # A dictionary containing all 16 LEC:s as keys and their intervals as values in a tuple
        # (min, max, interval, +-sigma)
        # Commented out LECS are for higher order approximations.
        # C_E and C_D does not do anything for cross section.
        self.lecs_dict = {
            'Ct_1S0np': (-0.1519, -0.1464, 0.0055 , 0.002),
            'Ct_1S0pp': (-0.1512, -0.1454, 0.0058, 0.002),
            'Ct_1S0nn': (-0.1518, -0.1463, 0.0053, 0.0021),
            'C_1S0': (2.4188, 2.5476, 0.1288 ,0.0511),
            'Ct_3S1': (-0.1807, -0.1348, 0.0459, 0.0032),
            'C3S1': (0.5037, 0.7396, 0.2359 ,0.0521),
            'C_3S1-3D1': (0.2792, 0.6574, 0.3782 ,0.0428),
            'C_3P0': (0.9924, 1.6343, 0.6419, 0.0428),
            'C_1P1': (0.0618, 0.6635, 0.6017, 0.0438),
            'C_3P1': (-0.9666, -0.4724, 0.4942, 0.0438),
            'C_3P2': (-0.7941, -0.6324, 0.1617, 0.0327),
            'c_D': (0.5933, 0.8348, 0.2415, 0.0833),
            'c_E': (-2.4019, -0.0893, 2.3126, 0.2282),
            'c1': (-0.8329, 0.2784, 1.1113,0.3043),
            #'c2': (2.7946, 5.3258, 1.0754),
            'c3': (-4.3601, -3.4474, 0.9128, 0.1506),
            'c4': (1.8999, 4.2353, 2.3354, 0.2179),
            #'d1+d2': (4.4636, 5.4505, 0.1378),
            #'d3': (-4.8549, -4.4583, 0.2302),
            #'d5': (-0.2992, 0.0233, 0.1407),
            #'d14-d15': (-10.3220, -9.6902, 0.2820),
            #'e14': (-0.3700, -9.1307, 2.4962),
            #'e15': (-11.9223, -9.1307, 2.4962),
            #'e16': (-0.6847, 7.4463, 4.2436),
            #'e17': (0.9322, 1.4896, 1.8143),
            #'e18': (-2.5068. 8.3777, 1.9022),
            }

        # Array with lec names to be used with dict above, for looping etc
        #TODO(DANIEL): Change this into something nicer and easier to work with.
        self.lecs_name = [
            'Ct_1S0np',
            'Ct_1S0pp',
            'Ct_1S0nn',
            'C_1S0',
            'Ct_3S1',
            'C3S1',
            'C_3S1-3D1',
            'C_3P0',
            'C_1P1',
            'C_3P1',
            'C_3P2',
            'c_D',
            'c_E',
            'c1',
            'c3',
            'c4',
            ]

        # Set up dimensions of sample size and lecs.
        self.interval = interval_width/2. # Split total interval into two sides.
        self.nbr_of_samples = nbr_of_samples
        self.nbr_of_lecs = len(self.lecs_dict.keys())
        self.nbr_of_points_1d = nbr_of_points_1d
        self.maxfun = maxfun
        self.maxiter = maxiter
        self.disp = disp
        
        # If we have no center interval input use default file as center_lecs
        if center_lecs is None:

            pot = 'N2LOsim'
            lam = 500
            cut = 290

            removed_lecs = (14, 17, 18, 19, 20, 21, 22, 23, 24, 25)
            lec_values = np.loadtxt(
                './resources/%s-%d-%d.LEC_values.txt' % (pot, lam, cut))
            lec_values = np.delete(lec_values, removed_lecs)

            self.center_lecs = np.reshape(lec_values, (1, len(lec_values)))

        # use center of the intervals as center_lecs if specified
        elif center_lecs == "center_of_interval":
            self.center_lecs = self.center_of_lecs_interval()
            self.center_lecs = np.reshape(self.center_lecs, (1, len(self.center_lecs)))
        else:
            self.center_lecs = np.reshape(center_lecs, (1, len(center_lecs)))
        
        

        # Array with the interval length in which each lec can vary with the current interval settings
        self.half_volume_length = np.zeros(self.nbr_of_lecs)
        for index, name in enumerate(self.lecs_name):
            self.half_volume_length[index] = self.lecs_dict[name][2]*self.interval
            
    def create_monospaced_lecs(self):
        """Returns monospaced grid of LECs"""

        range_list = []

        for idx in np.arange(len(self.center_lecs)):
            range_list.append((self.center_lecs[idx]-self.half_volume_length[idx],
                               self.center_lecs[idx]+self.half_volume_length[idx],
                               self.nbr_of_points_1d*1j))
                            
        lecs_grid = np.mgrid[[slice(i,j,k) for i,j,k in range_list]].reshape(len(range_list),-1).T

        lecs_grid = replace_superflous_lecs(lecs_grid)
        
        return lecs_grid


    
    """Create a set of lecs with a normal distribution in every dimension.
    Default is sigma=1/3 of interval
    Also cuts off the outliers outside of the volume, meaning you will get fewer rows than suspected
    """
    def create_gaussian_lecs(self):
        lec_samples = np.random.normal(loc=0, scale=0.3,
                size=(self.nbr_of_samples, self.nbr_of_lecs))
        delete_rows = []
        for i, row in enumerate(lec_samples):
            for value in row:
                if value > 1:
                    delete_rows.append(i)
                    break
        lec_samples = np.delete(lec_samples, delete_rows, axis=0)
        lec_samples = np.multiply(self.half_volume_length, lec_samples)
        lec_samples += self.center_lecs

        return lec_samples
    
    def create_lhs_lecs(self):
        """Returns matrix of LECS sampled using latin hypercube sampling"""
        lec_samples = pydoe.lhs(self.nbr_of_lecs, samples=self.nbr_of_samples)
        lec_min = self.center_lecs - self.half_volume_length
        lec_samples = 2*np.multiply(self.half_volume_length, lec_samples)

        lec_samples += lec_min

        lec_samples = self.replace_superflous_lecs(lec_samples)
        
        return lec_samples
        
    def create_random_uniform_lecs(self):
        """Creates matrix of random lec samples within the
        specified interval"""
        
        minvec = self.center_lecs - self.half_volume_length
        maxvec = self.center_lecs + self.half_volume_length
    
        lec_samples = np.random.uniform(minvec, maxvec, (self.nbr_of_samples, self.nbr_of_lecs))

        lec_samples = self.replace_superflous_lecs(lec_samples)
        
        return lec_samples

    def create_lecs_1dof(self,lecindex=0):
        """Returns matrix where only one lec is varied, the varied lec is given by lecindex.
        The varied points are equally spaced from the minimum value of the specified
        interval to the maximum value.
        """
        lec_samples = np.tile(self.center_lecs,[self.nbr_of_samples,1])

        minval = self.center_lecs[0,lecindex]-self.half_volume_length[lecindex]
        maxval = self.center_lecs[0,lecindex]+self.half_volume_length[lecindex]
        onedof_lec = np.linspace(minval, maxval, self.nbr_of_samples)

        lec_samples[:,lecindex] = onedof_lec
        lec_samples = self.replace_superflous_lecs(lec_samples)
        
        return lec_samples

    def create_maxmin_distance_lecs(self):
        "Creates matrix of LECs where the minimum distance between two points is maximized"
        
        nbr_of_dims = 14
        
        X = np.random.uniform(size=(self.nbr_of_samples, nbr_of_dims))

        # function that is minimized
        def min_distance(X):
            X = X.reshape(-1, nbr_of_dims)
            Y = pdist(X)
            mindist = np.amin(Y)
            return mindist * (-1)

        minval = 0
        maxval = 1

        # tuple of bounds for optimizer
        bnds = ((minval, maxval),) * X.size

        # options for optimizer
        opts = {'maxfun': self.maxfun, 'maxiter': self.maxiter, 'disp': self.disp}

        # optimization
        results = minimize(min_distance, X, method='l-bfgs-b', bounds=bnds, options=opts)

        points = results.x
        points = points.reshape(-1, nbr_of_dims)

        # insert columns for lecs C_E and C_D
        points = np.insert(points,11,0,axis=1)
        points = np.insert(points,11,0,axis=1)

        # transform intervals from 0,1 to specified lec intervals
        lec_min = self.center_lecs - self.half_volume_length
        lec_samples = 2*np.multiply(self.half_volume_length, points)
        lec_samples += lec_min

        lec_samples = self.replace_superflous_lecs(lec_samples)
        
        return lec_samples

    def center_of_lecs_interval(self):
        """Returns vector with center of total LEC intervals."""
        
        center_of_interval = np.zeros(self.nbr_of_lecs)
        # For each LEC, set center of interval to lec_min to lec_range/2
        for index, lec in enumerate(self.lecs_name):
            value = self.lecs_dict[lec]
            center_of_interval[index] = value[0] + value[2]/2
        return center_of_interval
        
    def replace_superflous_lecs(self, lec_samples):
        """Removed C_E and C_D since they do nothing."""
        lec_samples[:,11] = self.center_lecs[0,11]
        lec_samples[:,12] = self.center_lecs[0,12]
        
        return lec_samples

    @property
    def center_lecs(self):
        return self.center_lecs

    @center_lecs.setter
    def center_lecs(self, center_lecs):
        self.center_lecs = center_lecs
    @property
    def nbr_of_samples(self):
        return self.nbr_of_samples
    
    @nbr_of_samples.setter
    def nbr_of_samples(self, nbr_of_samples):
        self._nbr_of_samples = nbr_of_samples

        
        
