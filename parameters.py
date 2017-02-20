import numpy as np

class Parameters():
    """Handles input and generation of LECs."""

    def __init__():
        # A dictionary containing all 16 LEC:s as keys and their intervals as values in a tuple (min, max, +- sigma)
        #TODO(DANIEL): Complete this dict and ask Andreas about LECs. Which ones will we use?
        self.LEC_intervals = {
            'Ct_1S0np': (-0.1519, -0.1464, 0.002),
            'Ct_1S0pp': (-0.1512, -0.1454, 0.002),
            'Ct_1S0nn': (-0.1518, -0.1463, 0.0021),
            'C_1S0': (2.4188, 2-5476, 0.0511),
            'Ct_3S1': (-0.1807, -0.1348, 0.0032),
            'C_3S1-3D1': (),
            'C_3P0': (0.9924, 1.6343, 0.0428),
            # C_1P1?
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

        num_of_LECs = len(LEC_intervals.keys())
        num_of_points = 10j

        LEC_grid = np.mgrid[
            LEC_intervals['Ct_1S0np'][0]:LEC_intervals['Ct_1S0np'][1]:num_of_points,
            LEC_intervals['Ct_1S0pp'][0]:LEC_intervals['Ct_1S0pp'][1]:num_of_points,
            LEC_intervals['Ct_1S0nn'][0]:LEC_intervals['Ct_1S0nn'][1]:num_of_points,
            LEC_intervals['C_1S0'][0]:LEC_intervals['C_1S0'][1]:num_of_points,
            LEC_intervals['Ct_3S1'][0]:LEC_intervals['Ct_3S1'][1]:num_of_points,
            LEC_intervals['C_3S1-3D1'][0]:LEC_intervals['C_3S1-3D1'][1]:num_of_points,
            LEC_intervals['C_3P0'][0]:LEC_intervals['C_3P0'][1]:num_of_points,
            # C_1P1?
            LEC_intervals['C_3P1'][0]:LEC_intervals['C_3P1'][1]:num_of_points,
            LEC_intervals['C_3P2'][0]:LEC_intervals['C_3P2'][1]:num_of_points,
            LEC_intervals['c_D'][0]:LEC_intervals['c_D'][1]:num_of_points,
            LEC_intervals['c_E'][0]:LEC_intervals['c_E'][1]:num_of_points,
            LEC_intervals['c1'][0]:LEC_intervals['c1'][1]:num_of_points,
            LEC_intervals['c2'][0]:LEC_intervals['c2'][1]:num_of_points,
            LEC_intervals['c3'][0]:LEC_intervals['c3'][1]:num_of_points,
            LEC_intervals['c4'][0]:LEC_intervals['c4'][1]:num_of_points,
            LEC_intervals['d1+d2'][0]:LEC_intervals['d1+d2'][1]:num_of_points,
            LEC_intervals['d3'][0]:LEC_intervals['d3'][1]:num_of_points,
            LEC_intervals['d5'][0]:LEC_intervals['d5'][1]:num_of_points,
            LEC_intervals['d14-d15'][0]:LEC_intervals['d14-d15'][1]:num_of_points,
            LEC_intervals['e14'][0]:LEC_intervals['e14'][1]:num_of_points,
            LEC_intervals['e15'][0]:LEC_intervals['e15'][1]:num_of_points,
            LEC_intervals['e16'][0]:LEC_intervals['e16'][1]:num_of_points,
            LEC_intervals['e17'][0]:LEC_intervals['e17'][1]:num_of_points,
            LEC_intervals['e18'][0]:LEC_intervals['e18'][1]:num_of_points,
            ].reshape(num_of_LECs,-1).T
            
        
        
        pass
