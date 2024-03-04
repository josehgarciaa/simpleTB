import numpy as np
import grispy as gsp


class System():

    def __init__(self, site_list, lattice_vectors, upper_radii=0.42):

        self.site_list = site_list
        self.lattice_vectors = lattice_vectors
        self.neighbours = None

        self.hopping_calculator = _hopping_calculator
        self.onsite_calculator = _onsite_calculator

        self.onsite = None
        self.hopping = None

        # must be set to 1 because this will work on the coordinates
        self.grid_periodic = {0: (0, 1), 1: (0, 1), }  # 1: (0, 0)

        self.upper_radii=upper_radii
        self.lower_radii=0

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
            coord_xyz = xyz_to_local(self.site_list[site_key].xyz, self.lattice_vectors)

            site_xyz.append(coord_xyz)
        return np.array(site_xyz)

    def lattice_metric(self, site_0, centres, dim):
        """

        Computes the distance between site_0 and etch center
        Args:
            site_0 (Tensor): tensor with x,y,z in local coordinates
            centres (List[Tensors]):  list of the center coordinates in local coordinates
            dim (int):  dim of the site_0 integer representing the nr of elements in the vector site_0
                        not used rith now but required

        Returns: distances list of the distances to etch tensor

        """

        # concert site from lattice to xyz coordinates:
        s_xyz = local_to_xyz(site_0, self.lattice_vectors)

        distances = np.empty(len(centres))
        for idx, center in enumerate(centres):
            # mouve center back in real coordinates:
            c_xyz = local_to_xyz(center, self.lattice_vectors)

            # store the distance
            distances[idx] = np.linalg.norm(c_xyz - s_xyz)

        return distances

    def compute_neighbours(self):
        """
        Computes the neighbours
        Returns: Computes the neighbours and return them as a dictionary

        """

        site_coord = self.get_sites_coord_local()

        grid = gsp.GriSPy(site_coord,
                          periodic=self.grid_periodic,
                          metric=self.lattice_metric, )

        upper_radii = self.upper_radii
        lower_radii = self.lower_radii
        shell_dist, shell_ind = grid.shell_neighbors(centres=site_coord,
                                                     distance_lower_bound=lower_radii,
                                                     distance_upper_bound=upper_radii, )

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
        for site_a_id in self.site_list:
            for site_b_id in self.get_neighbours():
                if site_a_id!=site_b_id:
                    sa = self.site_list[site_a_id]
                    sb = self.site_list[site_b_id]
                    hopping_value = self.hopping_calculator(sa, sb)
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
            onsite.append([site_a_id, self.onsite_calculator(self.site_list[site_a_id])])

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

        for i, hop in enumerate(hopping):
            mat[hop[0]][hop[2]] = hop[2]

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
