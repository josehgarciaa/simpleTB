import numpy as np






def lattice_to_box(lat_vec):
    "LAT VEC AS COLUMN VECTORS"
    sizes = np.array([ np.sqrt(x.dot(x)) for x in lat_vec.T ] )
    normed_cell = np.norm(lat_vec.T, axis=0)
    normed_cell = np.acos(normed_cell.T@normed_cell.T)
    
    