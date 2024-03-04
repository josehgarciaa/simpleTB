"""

"""
import json

class Site():
    """
    Class for headlining local proprieties of  local proprieties of a system.
    """

    def __init__(self, site_id, label, real_xyz, prop):
        """

        Args:
            site_id (int):
            label (str):  string of the following structure : "Atom_Orbital_AnotherProp"
            xyz (Tensor or List): xyz coordinates.
            prop (dict):  dictionary with the site proprieties.
        """

        self.id = site_id
        self.label = label
        self.xyz = real_xyz
        self.prop = prop


    def to_dictionary(self):
        """

        Returns: site as a dictionary.

        """
        site={
            "site_id":self.id,
            "label":self.label,
            "xyz": self.xyz,
            "prop":self.prop
        }

        return site

    def to_json(self):
        """

        Returns: Site as json string

        """
        site = self.to_dictionary()
        json_string = json.dumps(site, indent=4)
        return json_string
