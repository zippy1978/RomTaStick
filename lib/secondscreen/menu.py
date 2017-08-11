
class MenuItem(object):

    SYMBOL_ARROW = 'arrow'

    action = None
    name = None
    symbol = None

    def __init__(self, name, action=None, symbol=None):
        self.action = action
        self.name = name
        self.symbol = symbol

class Menu(object):

    items = []
    title = None
    _selected_index = 0

    def __init__(self, items, title='Menu'):
        self.items = items
        self.title = title

    def select_next(self):
        if (self._selected_index + 1) >= len(self.items):
            self._selected_index = 0
        else:
            self._selected_index += 1

    def get_selected_index(self):
        return self._selected_index
