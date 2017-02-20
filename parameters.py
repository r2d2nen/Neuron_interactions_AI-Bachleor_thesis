import numpy as np

class Parameters():
    """Handles input and generation of LECs."""

    def __init__(self, interval, nbr_of_points):
        ### Set up parameter volume from supplied interval #LEC
        # A dictionary containing all 16 LEC:s as keys and their intervals as values in a tuple (min, max, +- sigma)
        #TODO(DANIEL): Ask Andreas about LECs. Which ones will we use and names are wrong?
        self.LEC_dict = {
            'Ct_1S0np': (-0.1519, -0.1464, 0.002),
            'Ct_1S0pp': (-0.1512, -0.1454, 0.002),
            'Ct_1S0nn': (-0.1518, -0.1463, 0.0021),
            'C_1S0': (2.4188, 2-5476, 0.0511),
            'Ct_3S1': (-0.1807, -0.1348, 0.0032),
            'C3S1': (0.5037, 0.7396, 0.0.0521),
            'C_3S1-3D1': (0.2792. 0.6574, 0.0428),
            'C_3P0': (0.9924, 1.6343, 0.0428),
            'C_1P1': (0.0618, 0.6635, 0.0438),
            'C_3P1': (-0.9666, -0.4724, 0.0438),
            'C_3P2': (-0.7941, -0.6324, 0.0327),
            'c_D': (0.5933, 0.8348, 0.0833),
            'c_E': (-2.4019, -0.0893, 0.2282),
            'c1': (-0.8329, 0.2784, 0.3043),
            'c2': (2.7946, 5.3258, 1.0754),
            'c3': (-4.3601, -3.4474, 0.1506),
            'c4': (1.8999, 4.2353, 0.2179),
            'd1+d2': (4.4636, 5.4505, 0.1378),
            'd3': (-4.8549, -4.4583, 0.2302),
            'd5': (-0.2992, 0.0233, 0.1407),
            'd14-d15': (-10.3220, -9.6902, 0.2820),
            'e14': (-0.3700, -9.1307, 2.4962),
            'e15': (-11.9223, -9.1307, 2.4962),
            'e16': (-0.6847, 7.4463, 4.2436),
            'e17': (0.9322, 1.4896, 1.8143),
            'e18': (-2.5068. 8.3777, 1.9022),
            }

        # Number of data points we want in our specified volume for each LEC
        self.nbr_of points = nbr_of_points

        # Dict
       # self.LEC_volume = 

        num_of_LECs = len(LEC_dict.keys())
        num_of_points = 10j

        LEC_grid = np.mgrid[
            LEC_dict['Ct_1S0np'][0]:LEC_dict['Ct_1S0np'][1]:num_of_points,
            LEC_dict['Ct_1S0pp'][0]:LEC_dict['Ct_1S0pp'][1]:num_of_points,
            LEC_dict['Ct_1S0nn'][0]:LEC_dict['Ct_1S0nn'][1]:num_of_points,
            LEC_dict['C_1S0'][0]:LEC_dict['C_1S0'][1]:num_of_points,
            LEC_dict['Ct_3S1'][0]:LEC_dict['Ct_3S1'][1]:num_of_points,
            LEC_dict['C_3S1-3D1'][0]:LEC_dict['C_3S1-3D1'][1]:num_of_points,
            LEC_dict['C_3P0'][0]:LEC_dict['C_3P0'][1]:num_of_points,
            LEC_dict['C_1P1'][0]:LEC_dict['C_3PO'][1]:num_of_points,
            LEC_dict['C_3P1'][0]:LEC_dict['C_3P1'][1]:num_of_points,
            LEC_dict['C_3P2'][0]:LEC_dict['C_3P2'][1]:num_of_points,
            LEC_dict['c_D'][0]:LEC_dict['c_D'][1]:num_of_points,
            LEC_dict['c_E'][0]:LEC_dict['c_E'][1]:num_of_points,
            LEC_dict['c1'][0]:LEC_dict['c1'][1]:num_of_points,
            LEC_dict['c2'][0]:LEC_dict['c2'][1]:num_of_points,
            LEC_dict['c3'][0]:LEC_dict['c3'][1]:num_of_points,
            LEC_dict['c4'][0]:LEC_dict['c4'][1]:num_of_points,
            LEC_dict['d1+d2'][0]:LEC_dict['d1+d2'][1]:num_of_points,
            LEC_dict['d3'][0]:LEC_dict['d3'][1]:num_of_points,
            LEC_dict['d5'][0]:LEC_dict['d5'][1]:num_of_points,
            LEC_dict['d14-d15'][0]:LEC_dict['d14-d15'][1]:num_of_points,
            LEC_dict['e14'][0]:LEC_dict['e14'][1]:num_of_points,
            LEC_dict['e15'][0]:LEC_dict['e15'][1]:num_of_points,
            LEC_dict['e16'][0]:LEC_dict['e16'][1]:num_of_points,
            LEC_dict['e17'][0]:LEC_dict['e17'][1]:num_of_points,
            LEC_dict['e18'][0]:LEC_intervals['e18'][1]:num_of_points,
            ].reshape(num_of_LECs,-1).T
            
        
    @property
    def nbr_of_points(self):
        return self.nbr_of_points
    
    @nbr_of_points.setter
    def nbr_of_points(self, nbr_of_points):
        self._nbr_of_points = nbr_of_points

    
