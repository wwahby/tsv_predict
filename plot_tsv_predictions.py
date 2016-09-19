import numpy as np
import tsv_predict as tp
import matplotlib.pyplot as pl

Ng = 1e6
rent_k = 1.8

max_tiers = 4
pmin = 0.0
pmax = 1
Np = 1e3
pvec = np.linspace(pmin, pmax, num=Np)

ntsv_mat = np.zeros( (max_tiers, int(Np)) )


for nind in range(max_tiers):
	num_tiers = nind+1
	for pind, rent_p in enumerate(pvec):
		( conn_tot, conn_per_layer, conn_to, conn_through ) = tp.calc_tsv_requirements(Ng, rent_k, rent_p, num_tiers)
		ntsv_mat[nind, pind] = conn_tot


colors = ["k", "b", "g", "r"]
fig = pl.figure(1)
pl.hold(True)

for nind in range(max_tiers):
	pl.plot(pvec, ntsv_mat[nind,:], color=colors[nind], linewidth=2)

#pl.yscale('log')
#pl.xlim([pmin, pmax])

pl.xlabel('Rent Exponent')
pl.ylabel('Number of TSVs Required')
pl.yscale('log')
#pl.xscale('log')
pl.savefig("rent_plot.png", transparent=True)
