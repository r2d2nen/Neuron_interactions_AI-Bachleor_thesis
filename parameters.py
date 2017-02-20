
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
            'C_3S1-3D1': ()
            'C_3P0': (),
            'C_3P1': (),
            'C_3P2': (),
            'c_D': (),
            'c_E': (),
            'c1': (),
            'c2': (),
            'c3': (),
            'c4': (),
            'd1+d2': (),
            'd3': (),
            'd5': (-0.2992, 0.0233, 0.1407),
            'd14-d15': (-10.3220, -9.6902, 0.2820),
            'e14': (-0.3700, -9.1307, 2.4962),
            'e15': (-11.9223, -9.1307, 2.4962),
            'e16': (-0.6847, 7.4463, 4.2436),
            'e17': (0.9322, 1.4896, 1.8143),
            'e18': (-2.5068. 8.3777, 1.9022),
            }
        pass
