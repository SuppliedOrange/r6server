"""MODIFIED VERSION OF CONSOLEMENU"""

from consolemenu.items import MenuItem


class ExternalItem(MenuItem):
    """
    A base class for items that need to do stuff on the console outside of the console menu.
    Sets the terminal back to standard mode until the action is done.
    Should probably be subclassed.
    """

    def __init__(self, text, menu=None, should_exit=False, menu_char=None, index_item_separator=None):
        # Here so Sphinx doesn't copy extraneous info from the superclass's docstring
        super(ExternalItem, self).__init__(text=text, menu=menu, should_exit=should_exit, menu_char=menu_char, index_item_separator=index_item_separator)

    def set_up(self):
        """
        This class overrides this method
        """
        self.menu.pause()
        self.menu.clear_screen()

    def clean_up(self):
        """
        This class overrides this method
        """
        self.menu.clear_screen()
        self.menu.resume()
