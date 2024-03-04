"""
Example of how to use simpleTB to simple  build your custom hamiltonian.
"""

from simpletb.read_xyz import parse_xyz_file
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
    Exampe of how to use simpleTB
    Returns:

    """
    print("Read xyz file")
    xyz_file = "examples/dummy_graphene/dummy_graphene.xyz"
    lattice_vectors, atom_types, coordinates = parse_xyz_file(xyz_file)

    print("lattice_vectors:", lattice_vectors)
    print("atom_types:", atom_types)
    print("coordinates:", coordinates)

    lattice_vectors=np.array([[26.88  ,      0.  ,        0.        ],
                              [ 0.   ,       7.    ,      0.        ],
                        [ 0.      ,    0.   ,      24.59512147]])


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


    def hopping_calculator(site_a, site_b):
        return 7


    def onsite_calculator(site_a):
        return 9


    material = System(syte_list, lattice_vectors, upper_radii=1 )

    material.hopping_calculator = hopping_calculator
    material.onsite_calculator = onsite_calculator

    hoping_onsite_matrix = material.get_hopping_onsite_matrix()
    print("neighbours:", material.get_neighbours())
    print("hopping_onsite:\n", hoping_onsite_matrix)

    plot_heatmap(hoping_onsite_matrix)
    plt.show()



main()