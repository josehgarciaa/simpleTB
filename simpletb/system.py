
import numpy as np

from scipy.spatial.distance import cdist
import numpy as np
import grispy as gsp
from .site import Site


class System():

    def __init__(self, site_list=None, lattice_vectors=None, dimensions=(1 ,1 ,1), **kwargs):
        """

        Args:
            site_list ():
            lattice_vectors ():
        """
        self.neighbours = None
        self.hopping_function = None
        self.onsite_onsite = None
        self.onsite_list = None
        self.hopping_list= None


        self.site_list = site_list
        self.lattice_vectors = lattice_vectors
        self.dimensions= dimensions





    def get_site_coordinates(self):
        """

        Returns: site coordinates in fractional coordinates and as column vectors

        """

        return self.__cartesian_to_fractional( self.site_list.coordinates())


    def get_sites(self):
        return self.site_list.get_sites()

    def set_onsite_function(self, onsite_function):
        """
        A function that takes as the argument an object of type Site and returns a real number.
        Args:
            onsite_function (Callable[[Site], float]): A function that accepts a Site object and returns a float.
        """
        # This is a simple check to see if the function can accept a Site instance and return a float.
        # More sophisticated or specific checks might be required depending on the use case.
        try:
            assert isinstance(onsite_function(Site()), float), "Function does not return a float"
        except AssertionError as e:
            raise TypeError \
                ("onsite_function must be a callable that accepts a Site instance and returns a float.") from e
        self.onsite_function = onsite_function
        return True

    def set_hopping_function(self, hopping_function):
        """
        A function that takes as the argument an object of two objects Site_i and Site_j and returns a complex number.
        Args:
            hopping_function (Callable[[Site,Site], complex]): A function that accepts two  Site objects and returns a complex.
        """
        # This is a simple check to see if the function can accept a Site instance and return a float.
        # More sophisticated or specific checks might be required depending on the use case.
        try:
            assert isinstance(hopping_function(Site() ,Site()), complex), "Function does not return a float"
        except AssertionError as e:
            raise TypeError \
                ("onsite_function must be a callable that accepts a Site instance and returns a float.") from e
        self.hopping_function = hopping_function
        return True

    def get_neighbours(self):
        """
        Returns: Returns the neighbours if they are computed if not it computes them an after that it returns them.
        """
        if self.neighbours is not None:
            return self.neighbours
        else:
            return self.compute_neighbours()




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
                    hopping_value = self.hopping_function(self, sa, sb)
                    hoppings.append([site_a_id, site_b_id, hopping_value])

        self.hopping_list = hoppings
        return self.hopping_list

    def compute_onsite(self):
        """
        Computes the onsite for etch site
        Returns: [[site, onsite],...]

        """
        onsite_list = []
        for site_a_id in self.site_list:
            onsite_list.append([site_a_id, self.onsite_function(self, self.site_list[site_a_id])])
        self.onsite_list = onsite_list

        return self.onsite_list

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


    def __cartesian_to_fractional(self, cart):
        """
        Convert a set of cartesian coordinates (provided as column vectors) into fractional coordinates
        Args:
            cart:  a set of cartesian coordinates (provided as column vectors)

        Returns: fractional coordinates

        """

        return np.linalg.inv(self.lattice_vectors ) @cart

    def __fractional_to_cartesian(self, frac):
        """
        convert a set of fractional coordinates (provided as column vectors) into cartesian coordinates
        Args:
            frac: a set of fractional coordinates (provided as column vectors)

        Returns: cartesian coordinates

        """

        return self.lattice_vectors @frac

