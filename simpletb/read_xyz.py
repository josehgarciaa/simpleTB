"""
Read from xyz file
"""
from ase.cell import Cell
from ase.io import read

from ase.io import read
import numpy as np




def parse_xyz_file(filename):
    """

    Args:
        filename (str):  path theo the xyz file with the system information

    Returns: lattice vectors, atom:types, atomic coordinates

    """
    atoms = read(filename, format='xyz')
    atom_types = atoms.get_chemical_symbols()
    coordinates = atoms.get_positions()
    lattice_vectors= atoms.get_cell()


    return lattice_vectors, atom_types, coordinates


