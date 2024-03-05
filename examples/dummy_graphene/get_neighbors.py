from simpletb import System
from simpletb.parser import struct_from_xyz
from simpletb.site_list import SiteList
import numpy as np

import grispy as gsp


#Read sites and cell from xyz file
lattice_vectors, atom_labels, atom_coordinates = struct_from_xyz("dummy_graphene.xyz")

#construct a site list 
site_list = SiteList(atom_labels, atom_coordinates)

#Pass the sites and lattice vectors to the system
syst = System(lattice_vectors=lattice_vectors, site_list=site_list)

#Brute force calculation
point_grid = (site_list.coordinates().T)[:10]
#grid = gsp.GriSPy(point_grid)
#centres = point_grid
#dist, ind = grid.bubble_neighbors(centres, distance_upper_bound=1.0)
#print(ind)


data = np.random.uniform(size=(10, 3))*1e-7 + point_grid.reshape(-1,3)

grid = gsp.GriSPy(data)
centres = data
dist, ind = grid.bubble_neighbors(centres, distance_upper_bound=1.0)
print(ind, data)

#syst.ComputeNeighbors(0.3)
#syst.SetHoppingFunction( hopping)
