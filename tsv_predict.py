import numpy as np
import argparse

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("Ng", type=float, help="Total number of logic gates in the design")
	parser.add_argument("k", type=float, help="Rent constant for the design")
	parser.add_argument("p", type=float, help="Rent exponent for the design")
	parser.add_argument("tiers", type=int, help="Number of tiers in the 3D stack")
	args = parser.parse_args()

	Ng = args.Ng
	k = args.k
	p = args.p
	tiers = args.tiers
	( conn_tot, conn_per_layer, conn_to, conn_through ) = calc_tsv_requirements(Ng, k, p, tiers)

	fstr_header = "{0:>14s}  {1:>14s}  {2:>14s}  {3:>14s}"
	fstr_data = "{0:>14.3g}  {1:>14.3f}  {2:>14.3f}  {3:>14d}"
	header = fstr_header.format("Num Gates", "Rent k", "Rent p", "Num Tiers")
	dstr = fstr_data.format(Ng, k, p, int(tiers))
	print(header)
	print(dstr)
	print()

	hstr = "{0:>14s}  {1:>14s}  {2:>14s}  {3:>14s}"
	fstr_data = "{0:>14d}  {1:>14.3g}  {2:>14.3g}  {3:>14.3g}"
	header = hstr.format("Tier", "Vias_tot", "Vias_to", "Vias_through")
	print(header)
	for tier in range(tiers):
		dstr = fstr_data.format(tier, conn_per_layer[tier], conn_to[tier], conn_through[tier])
		print(dstr)

	print()
	print( "{0:>14s}".format("Total Vias") )
	print( "{0:>14.3g}".format(conn_tot) )



def get_total_tsvs_for_diff_num_tiers(Ng, k, p, max_tiers):
	# Will return a vector of the number of TSVs needed for this design implemented
	# with n=1:max_tiers tiers

	conn_tot_vec = np.zeros((max_tiers))
	conn_per_layer_list = []
	conn_to_list = []
	conn_through_list = []
	for nind in range(max_tiers):
		tiers = nind+1
		( conn_tot, conn_per_layer, conn_to, conn_through ) = calc_tsv_requirements(Ng, k, p, tiers)
		conn_tot_vec[nind] = conn_tot
		conn_per_layer_list.append(conn_per_layer)
		conn_to_list.append(conn_to)
		conn_through_list.append(conn_through)

	return (conn_tot_vec, conn_per_layer_list, conn_to_list, conn_through_list)



def calc_Tac(Ns, k, p, tier1_ind, tier2_ind):
	bac = max(0,tier2_ind - tier1_ind -1) # bac = number of tiers BETWEEN tiers 1 and 2
	Tac = 2*k*Ns**p * (bac + 1) - k*Ns**p * (bac + 2)**p - k*(bac*Ns)**p

	return Tac

def calc_connections_through_tier(Ns, k, p, tier_ind, num_tiers):
	conn_through = 0
	for bot_tier in range(tier_ind):
		for top_tier in range(tier_ind+1,num_tiers):
			Tac = calc_Tac(Ns, k, p, bot_tier, top_tier)
			conn_through += Tac

	return conn_through

def calc_connections_through(Ns, k, p, num_tiers):
	conn_through = np.zeros(num_tiers)
	for tier in range(num_tiers):
		conn_through[tier] = calc_connections_through_tier(Ns, k, p, tier, num_tiers)

	return conn_through

def calc_connections_to_tier(Ns, k, p, tier, num_tiers):
	# Assumes F2B bonding style
	#    Connections to tiers below do not require TSVs
	#    Connections to tiers above require TSVs

	conn_to = 0
	for dest_tier in range(tier+1,num_tiers):
		conn_to += calc_Tac(Ns, k, p, tier, dest_tier)

	return conn_to


def calc_connections_to(Ns, k, p, num_tiers):
	conn_to = np.zeros(num_tiers)
	for tier in range(num_tiers):
		conn_to[tier] = calc_connections_to_tier(Ns, k, p, tier, num_tiers)

	return conn_to


def calc_tsv_requirements(Ng, k, p, num_tiers):
	Ns = Ng/num_tiers
	conn_to = calc_connections_to(Ns, k, p, num_tiers)
	conn_through = calc_connections_through(Ns, k, p, num_tiers)
	conn_per_layer = conn_to + conn_through # Total TSVs in each layer
	conn_tot = np.sum(conn_per_layer)

	return ( conn_tot, conn_per_layer, conn_to, conn_through )


if (__name__ == "__main__"):
	main()
