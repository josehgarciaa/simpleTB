

import numpy as np

from simpletb.models.graph import SpatialGraph  
from scipy.spatial.distance import cdist

import grispy as gsp


from simpletb import SiteList

class System():
    """ Storage and handle the momentum-space model and structural information of the system  

    Args:
        dimensions (tuple): A three integer tuple that defines the dimensions of the system in terms of repeating unit cells. 
        
    :Keyword Arguments:

        The arguments are presented in order of preference, i.e, w90_inp will be used over model. 
        
        w90_inp (str): The filename of a Wannier90 input file. Calling this argument will look for the label_hr.dat and label.xyz files in the same directory

    Attributes:
        dimensions (tuple): A three integer tuple that defines the dimensions of the system in terms of repeating unit cells.

    """
    
    dimensions= None;
    #lattice   = Lattice();
    ham_fun   = None;
    rec_lat   = None; 
    ham_op    = None;
    Uop       = None;
    basis     = "bloch"
    sitelist  = SiteList()

    def __init__(self, dimensions=(1,1,1), **kwargs):

        self.dimensions= dimensions ;
        #self.rec_lat   = self.ReciprocalLattice()

        #When the user submit a Wannier90 input, use it to initialice the system
        if "graph" in kwargs:
            cell, points = kwargs["graph"]
            self.syst = SpatialGraph(cell, points)

    def ComputeNeighbors(self, cutoff):
        self.cutoff = cutoff
        def lattice_metric(c0, centres, dim):
            c0 = c0.reshape((-1, dim))
            d = cdist(c0, centres).reshape((-1,))
            d = cdist(c0@self.syst.metric, centres).reshape((-1,))
            return d

        print(self.syst.metric)
        periodic = {0: (0, float(self.dimensions[0])),
                    1: (1, float(self.dimensions[1])),
                    2: (2, float(self.dimensions[2]))}

        point_grid = self.syst.frac_points.T
        grid = gsp.GriSPy(point_grid, metric=lattice_metric)
        centres = np.array([[0.,0.,0.]])
        dist, ind = grid.bubble_neighbors(centres, distance_upper_bound=self.cutoff )
        print(self.cutoff,dist, ind)


import numpy as np
import grispy as gsp
from simpletb.site import Site 

class System():

    def __init__(self, site_list, lattice_vectors, dimensions=(1,1,1), **kwargs):
        """

        Args:
            site_list ():
            lattice_vectors ():
        """

        self.site_list = site_list
        self.lattice_vectors = lattice_vectors
        self.neighbours = None

        self.hopping_function = _hopping_calculator
        self.onsite_onsite = _onsite_calculator

        self.onsite_list = None
        self.hopping_list= None

        self.dimensions= dimensions ;

        # Prescribe by the dimensionality f the supercell
        
        periodic = {0: (0, float(self.dimensions[0])),
                    1: (1, float(self.dimensions[1])),
                    2: (2, float(self.dimensions[2]))}



    def set_onsite_function(self, onsite_function):
        """
        A function that take as the argument an object of type Site and return a real number
        Args:
            Site():
        Return
            Real number
        """        
        try:
            x = onsite_function( Site() )
        except:
            print("Not a valid onsite-function")
            
        self.onsite_function = onsite_function

    def set_hopping_function(self, onsite_function):
        self.hopping_function = hopping_function

    def get_onsite(self):
        """

        Returns: the onsite and computes them if they are not computed yet

        """
        if self.onsite is not None:
            return self.onsite
        else:
            return self.compute_onsite()

    def get_hopping(self):
        """

        Returns: Returns the hopping and computes them if they are not computed yet.

        """

        if self.hopping is not None:
            return self.hopping
        else:
            return self.compute_hopping()

    def get_neighbours(self):
        """

        Returns: Returns the neighbours if they are computed if not it computes them an after that it returns them.

        """

        if self.neighbours is not None:
            return self.neighbours
        else:
            return self.compute_neighbours()

    def get_sites_coord_local(self):
        """
        Computes the sites coordinates in local coordinates.
        Returns: np.array of sites coordinates

        """

        site_xyz = []

        for site_key in self.site_list.keys():
            # coord_xyz = xyz_to_local(self.site_list[site_key].xyz, self.lattice_vectors)
            coord_xyz = self.site_list[site_key].xyz
            site_xyz.append(coord_xyz)
        return np.array(site_xyz)

    # def lattice_metric(self, site_0, centres, dim):
    #     """
    #
    #     Computes the distance between site_0 and etch center
    #     Args:
    #         site_0 (Tensor): tensor with x,y,z in local coordinates
    #         centres (List[Tensors]):  list of the center coordinates in local coordinates
    #         dim (int):  dim of the site_0 integer representing the nr of elements in the vector site_0
    #                     not used rith now but required
    #
    #     Returns: distances list of the distances to etch tensor
    #
    #     """
    #
    #     # concert site from lattice to xyz coordinates:
    #     # s_xyz = local_to_xyz(site_0, self.lattice_vectors)
    #     s_xyz = site_0
    #
    #     distances = np.empty(len(centres))
    #
    #     # TODO:
    #     # Do it with matrix multiplication so it will be faster
    #     for idx, center in enumerate(centres):
    #         # mouve center back in real coordinates:
    #         # c_xyz = local_to_xyz(center, self.lattice_vectors)
    #         c_xyz = center
    #         # store the distance
    #         distances[idx] = np.linalg.norm(c_xyz - s_xyz)
    #
    #     print("d:", distances)
    #     return distances

    def compute_neighbours(self):
        """
        Computes the neighbours
        Returns: Computes the neighbours and return them as a dictionary

        """

        site_coord = self.get_sites_coord_local()

        grid = gsp.GriSPy(site_coord,
                          periodic=self.grid_periodic,
                          # metric=self.lattice_metric,
                          )

        upper_radii = self.upper_radii
        lower_radii = self.lower_radii
        # Go from buble to shell
        #bubble
        # shell_dist, shell_ind = grid.bubble_neighbors(centres=site_coord,
        #                                               # distance_lower_bound=lower_radii,
        #                                               distance_upper_bound=upper_radii, )
        shell_dist, shell_ind = grid.nearest_neighbors(centres=site_coord[:2],
                                                     n=1 )

        print("sd:", shell_dist)
        print("shell_ind:", shell_ind)
        neighbours = {}

        for sit_key in self.site_list.keys():
            neighbours[sit_key] = shell_ind[sit_key]

        self.neighbours = neighbours
        return neighbours

    def compute_hopping(self):
        """
        Computes the hopping for the entire system.
        Returns: [[(site1, site2), hopping_value]...]

        """
        hoppings = []
        neighbours = self.get_neighbours()
        for site_a_id in self.site_list.keys():
            for site_b_id in neighbours[site_a_id]:

                if site_a_id != site_b_id:
                    sa = self.site_list[site_a_id]
                    sb = self.site_list[site_b_id]
                    hopping_value = self.hopping_calculator(self, sa, sb)
                    hoppings.append([site_a_id, site_b_id, hopping_value])

        self.hopping = hoppings
        return hoppings

    def compute_onsite(self):
        """
        Computes the onsite for etch site
        Returns: [[site, onsite],...]

        """
        onsite = []
        for site_a_id in self.site_list:
            onsite.append([site_a_id, self.onsite_calculator(self, self.site_list[site_a_id])])

        self.onsite = onsite

        return onsite

    def get_hopping_onsite_matrix(self):
        """
        Puts the hopping and onsite on a matrix.
        Returns: matrix of hopping and onsite

        """
        onsite = self.get_onsite()
        hopping = self.get_hopping()

        mat = np.zeros([len(onsite), len(onsite)])
        for i, os in enumerate(onsite):
            mat[os[0]][os[0]] = os[1]

        print("hopping", hopping)
        for i, hop in enumerate(hopping):
            mat[hop[0]][hop[1]] = hop[2]

        return mat


def _hopping_calculator(self, site_a, site_b):
    return 2


def _onsite_calculator(self, site_a):
    return 1


def local_to_xyz(local_vector, lattice_vectors):
    """
    Converts local coordinates to coordinates in real space (xyz).

    Args:
        local_vector (numpy.ndarray): The local coordinates.
        lattice_vectors (numpy.ndarray): The lattice vectors.

    Returns:
        numpy.ndarray: The corresponding coordinates in real space (xyz).
    """
    inverse_lattice = np.linalg.inv(lattice_vectors)
    xyz_vector = np.dot(local_vector, inverse_lattice)
    return xyz_vector


def xyz_to_local(xyz_vector, lattice_vectors):
    """
    Converts coordinates from real space (xyz) to local coordinates.

    Args:
        xyz_vector (numpy.ndarray): The coordinates in real space (xyz).
        lattice_vectors (numpy.ndarray): The lattice vectors.

    Returns:
        numpy.ndarray: The corresponding local coordinates.
    """
    inverse_lattice = np.linalg.inv(lattice_vectors)
    local_vector = np.dot(xyz_vector, inverse_lattice)
    return local_vector
