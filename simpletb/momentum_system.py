import numpy as np
from simpletb.models.graph import SpatialGraph
from scipy.spatial.distance import cdist
import grispy as gsp
from .site_list import SiteList

class MomentumSystem():
    """ Storage and handle the momentum-space model and structural information of the system

    Args:
        dimensions (tuple): A three integer tuple that defines the dimensions of the system in terms of repeating unit cells.

    :Keyword Arguments:

        The arguments are presented in order of preference, i.e, w90_inp will be used over model.

        w90_inp (str): The filename of a Wannier90 input file. Calling this argument will look for the label_hr.dat and label.xyz files in the same directory

    Attributes:
        dimensions (tuple): A three integer tuple that defines the dimensions of the system in terms of repeating unit cells.

    """

    dimensions = None
    # lattice   = Lattice();
    ham_fun = None
    rec_lat = None
    ham_op = None
    Uop = None
    basis = "bloch"
    sitelist = SiteList()

    def __init__(self, dimensions=(1, 1, 1), **kwargs):
        self.dimensions = dimensions;
        # self.rec_lat   = self.ReciprocalLattice()

        # When the user submit a Wannier90 input, use it to initialice the system
        if "graph" in kwargs:
            cell, points = kwargs["graph"]
            self.syst = SpatialGraph(cell, points)

    def ComputeNeighbors(self, cutoff):
        self.cutoff = cutoff

        def lattice_metric(c0, centres, dim):
            c0 = c0.reshape((-1, dim))
            d = cdist(c0, centres).reshape((-1,))
            d = cdist(c0 @ self.syst.metric, centres).reshape((-1,))
            return d

        print(self.syst.metric)
        periodic = {0: (0, float(self.dimensions[0])),
                    1: (1, float(self.dimensions[1])),
                    2: (2, float(self.dimensions[2]))}

        point_grid = self.syst.frac_points.T
        grid = gsp.GriSPy(point_grid, metric=lattice_metric)
        centres = np.array([[0., 0., 0.]])
        dist, ind = grid.bubble_neighbors(centres, distance_upper_bound=self.cutoff)
        print(self.cutoff, dist, ind)
