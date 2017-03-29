import numpy as np
from nsoptcaller import NsoptCaller
from parameters import Parameters
from gaussfit import Gaussfit


interval = 1
samples = 60
energy = (1, 20)
kernel = 'RBF'
LEC_LENGTH = 16
lengthscale = 1.

param = Parameters(interval, samples, center_lecs='center_of_interval')
nsopt = NsoptCaller()
gauss = Gaussfit()

lecs = param.create_lhs_lecs(energy_interval=energy)
print(lecs)
energies = lecs[:,-1]
print(energies)
lecs = lecs[:,0:-1]

observables = nsopt.get_nsopt_observable(energies, LECM=lecs)
print('----------------------------------------------------------------------------------------------------')
print(observables)
print(np.size(observables))
print('----------------------------------------------------------------------------------------------------')

val_lecs = np.split(lecs,2)[0]
val_energy = np.split(energies,2)[0]
val_obs = np.split(observables,2)[0]

train_lecs = np.split(lecs,2)[1]
train_energy =np.split(energies,2)[1]
train_obs = np.split(observables,2)[1]

gauss.set_gp_kernel(kernel=kernel, in_dim=LEC_LENGTH, lengthscale=lengthscale,
                    multi_dim=True)
gauss.populate_gp_model(train_obs, np.hstack((train_lecs, train_energy)), rescale=False)
gauss.optimize()

mod_obs, mod_var = gauss.calculate_valid(np.hstack(val_lecs,val_energy))

gauss.plot_predicted_actual(mod_obs, val_obs, mod_var, 'hej', 'hej')


