"""
Example of how to use simpleTB to simple  build your custom hamiltonian.
"""

from simpletb.parser.structure import read_xyz
from simpletb import System, Site
import periodictable
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
    lattice_vectors, atom_types, coordinates = read_xyz(xyz_file)

    print("lattice_vectors:", lattice_vectors)
    print("atom_types:", atom_types)
    print("coordinates:", coordinates)

    # Construct the system elements:
    syte_list = {}
    for i, xyz in enumerate(coordinates):
        syte_list[i] = Site(site_id=i,
                            label=str(atom_types[i]) + "_",
                            real_xyz=xyz,
                            prop={
                                "atom_nr": periodictable.elements.symbol(str(atom_types[i])).number,
                                "dummy": "73",
                            })

    def hopping_calculator(self, site_a, site_b):
        t10 = -2.414
        t20 = -0.168

        r = np.linalg.norm(site_a.xyz - site_b.xyz)
        if r <= (1 + np.sqrt(3)) * 1.24 / 2:
            t = t10 * np.exp(1.847 * (r - 1.24))
        elif r <= (2 + np.sqrt(3)) * 1.24:
            t = t20 * np.exp(-0.168 * (r - 1.24 * np.sqrt(3)))
        else:
            t = 0

        return t

    def onsite_calculator(self, site_a):

        onsite = 9
        simbol = site_a.label.split("_")[0]
        if simbol == "C":
            onsite = 2
        else:
            onsite = 3
        return onsite

    material = System(syte_list, lattice_vectors, upper_radii=10, lower_radii=0.001)

    material.hopping_calculator = hopping_calculator
    material.onsite_calculator = onsite_calculator

    hoping_onsite_matrix = material.get_hopping_onsite_matrix()
    print("neighbours:", material.get_neighbours())
    print("hopping_onsite:\n", hoping_onsite_matrix)

    plot_heatmap(hoping_onsite_matrix)
    plt.show()


if __name__ == "__main__":
    main()
