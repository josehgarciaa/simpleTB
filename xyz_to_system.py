"""
Example of how to use simpleTB to simple  build your custom hamiltonian.
"""

from simpletb.parser import struct_from_xyz
from simpletb.neighbors import get_neighbor_indexes
from simpletb import System, SiteList
import numpy as np
import matplotlib.pyplot as plt


# Some plotting functions for visualization
def plot_heatmap(matrix):
    plt.figure(figsize=(8, 6))
    plt.imshow(matrix, cmap='viridis', interpolation='nearest')
    plt.colorbar()
    plt.title('Heatmap of Matrix')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.show()


def main():
    """
    Example of how to use simpleTB
    Returns:

    """
    print("Read xyz file")
    xyz_file = "examples/dummy_graphene/dummy_graphene.xyz"
    lattice_vectors, atom_types, coordinates = struct_from_xyz(xyz_file)

    print("lattice_vectors:", lattice_vectors)
    print("atom_types:", atom_types)
    print("coordinates:", coordinates)

    # Put the system into a site list:
    site_list = SiteList(atom_types, coordinates)
    print("Nr of sites:", len(site_list.site_list))
    print("Site list:", site_list)

    def hopping_calculator(system, site_a, site_b):
        """

        Args:
            system:
            site_a:
            site_b:

        Returns:

        """
        t10 = -2.414
        t20 = -0.168

        r = np.linalg.norm(site_a.coord - site_b.coord)
        if r <= (1 + np.sqrt(3)) * 1.24 / 2:
            t = t10 * np.exp(1.847 * (r - 1.24))
        elif r <= (2 + np.sqrt(3)) * 1.24:
            t = t20 * np.exp(-0.168 * (r - 1.24 * np.sqrt(3)))
        else:
            t = 0.0

        return t + 0j

    def onsite_calculator(system, site_a):
        """

        Args:
            system:
            site_a:

        Returns:

        """

        simbol = site_a.label.split("_")[0]
        if simbol == "C":
            onsite = 2
        else:
            onsite = 3.0
        return onsite

    # Build the material:
    material = System(site_list, lattice_vectors)

    material.set_onsite_function(onsite_calculator)
    material.set_hopping_function(hopping_calculator)

    def get_neighbours(system):
        """
        Function to decide the neighbours
        Args:
            system: System in witch we need to compute the neighbours

        Returns: list of neighbours []

        """
        return get_neighbor_indexes(system, cutoff=5, pbc=(True, True, False))

    material.set_compute_neighbours(get_neighbours)

    hoping_onsite_matrix = material.get_hopping_onsite_matrix()
    print("neighbours:", material.get_neighbours())
    print("hopping_onsite:\n", hoping_onsite_matrix)
    hoping_onsite_matrix_real=hoping_onsite_matrix.real
    plot_heatmap(hoping_onsite_matrix_real)
    plt.show()


if __name__ == "__main__":
    main()
