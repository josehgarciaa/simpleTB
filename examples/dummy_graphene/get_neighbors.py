from simpletb import System
from simpletb.parser import struct_from_xyz
from simpletb.site_list import SiteList
import numpy as np
import grispy as gsp
from MDAnalysis.lib.distances import distance_array


#Read sites and cell from xyz file
lattice_vectors, atom_labels, atom_coordinates = struct_from_xyz("dummy_graphene.xyz")

#construct a site list 
site_list = SiteList(atom_labels, atom_coordinates)

#Pass the sites and lattice vectors to the system
syst = System(lattice_vectors=lattice_vectors, site_list=site_list)
import copy


def create_supercell(system, pbc = [True,True,True]):
    scsites= SiteList()
    lat = system.lattice_vectors.T
    N0 = (-1,0,1) if pbc[0] else (0,)
    N1 = (-1,0,1) if pbc[1] else (0,)
    N2 = (-1,0,1) if pbc[2] else (0,)

    for _site in system.get_sites():
        for n0 in N0:
            for n1 in N1:
                for n2 in N2:
                    site = copy.copy(_site)
                    site.set_coord( site.get_coord() + n0*lat[0]+ n1*lat[1]+ n2*lat[2]  )
                    scsites.site_list.append(site)       
    return scsites

scsites = create_supercell(syst, pbc=(True,True, False))
from scipy.spatial import cKDTree
tree = cKDTree(scsites.coordinates().T)


cutoff = 3.0
for site in syst.get_sites():
    indices = tree.query_ball_point(site.coord, r=cutoff)
    print(site.uid, scsites.get_uids(indices))




#sc_list.coordinates().T
#for point in points:
#        indices = tree.query_ball_point(point, r=cutoff)
#        # Filter out the point itself and duplicates from periodic images
#        filtered = [i for i in indices if np.linalg.norm(supercell[i] - point) <= cutoff and np.linalg.norm(supercell[i] - point) != 0]
#        neighbors.append(filtered)
#    return neighbors

                

#def lattice_to_box(lat_vec):
#    "LAT VEC AS COLUMN VECTORS"
##    sizes = np.array([ np.sqrt(x.dot(x)) for x in lat_vec.T ] )
#    cosangles = np.diag(1/sizes)@lat_vec.T
#    return [sizes[0],sizes[1],sizes[2], np.arccos(cosangles[0,1])*180/np.pi, np.arccos(cosangles[0,2])*180/np.pi, np.arccos(cosangles[1,2])*180/np.pi]
    #normed_cell = np.normalize(lat_vec.T, axis=0)
    #normed_cell = np.acos(normed_cell.T@normed_cell.T)
#distance_matrix = distance_array(point_grid, point_grid, box=lattice_to_box(lattice_vectors) )
#cutoff = 3.0
#neighbors = np.where((distance_matrix < cutoff) & (distance_matrix != 0))
#print(neighbors)






#grid = gsp.GriSPy(point_grid)
#centres = point_grid
#dist, ind = grid.bubble_neighbors(centres, distance_upper_bound=1.0)
#print(ind)


#data = np.random.uniform(size=(10, 3))*1e-7 + point_grid.reshape(-1,3)

#grid = gsp.GriSPy(data)
#centres = data
#dist, ind = grid.bubble_neighbors(centres, distance_upper_bound=1.0)
#print(ind, data)

#syst.ComputeNeighbors(0.3)
#syst.SetHoppingFunction( hopping)
