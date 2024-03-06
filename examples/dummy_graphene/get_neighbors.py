from simpletb import System
from simpletb.parser import struct_from_xyz
from simpletb.site_list import SiteList
from simpletb.neighbors import get_neighbor_indexes

# Read sites and cell from xyz file
lattice_vectors, atom_labels, atom_coordinates = struct_from_xyz("dummy_graphene.xyz")

# construct a site list
site_list = SiteList(atom_labels, atom_coordinates)

# Pass the sites and lattice vectors to the system
syst = System(lattice_vectors=lattice_vectors, site_list=site_list)

print(get_neighbor_indexes(syst, cutoff=3, pbc=(True, True, False)))
