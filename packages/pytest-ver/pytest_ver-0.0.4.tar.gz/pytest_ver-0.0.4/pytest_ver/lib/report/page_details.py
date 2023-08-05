from .footer import Footer
from .header import Header
from .. import services


# -------------------
class PageDetails:
    # -------------------
    def __init__(self):
        self.orientation = 'portait'
        self.page_size = 'letter'
        self.header = Header()
        self.footer = Footer()

    # -------------------
    def __setitem__(self, item, value):
        if item == 'orientation':
            self.orientation = value
            return

        if item == 'page_size':
            self.page_size = value
            return

        services.logger.err(f'bad item name: {item}')
        services.harness.abort()

    # -------------------
    def __getitem__(self, item):
        if item == 'header':
            return self.header

        if item == 'footer':
            return self.footer

        if item == 'orientation':
            return self.orientation

        if item == 'page_size':
            return self.page_size

        services.logger.err(f'bad item name: {item}')
        services.harness.abort()
