from .site import Site


class SiteList:
    """
    Class for Handling groups of sites local proprieties of  local proprieties of a system.
    """

    def __init__(self):
        """

        """

        self.site_list = []

    def add(self, site: Site):
        """

        Args:
            site: A site object

        Returns:
            Add a site to the list.
            Return site_list with the extra element.
        """
        self.site_list.append(site)

        return self.site_list
