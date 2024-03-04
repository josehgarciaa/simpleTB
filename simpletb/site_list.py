from simpletb import Site



class SiteList:
    """
    Class for Handling groups of sites local proprieties of  local proprieties of a system.
    """

    def __init__(self):
        """

        Args:
            site_id (int):
            label (str):  string of the following structure : "Atom_Orbital_AnotherProp"
            xyz (Tensor or List): xyz coordinates.
            prop (dict):  dictionary with the site proprieties.
        """

        self.site_list = []

    def add(self, site):
        """
        Returns: Add a site to the list
        """
        self.site_list.append(site)
