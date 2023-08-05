from .. import services


# -------------------
class Header:
    # -------------------
    def __init__(self):
        self.left = ''
        self.middle = ''
        self.right = ''

    # -------------------
    def __setitem__(self, item, value):
        if item == 'left':
            self.left = value
            return

        if item == 'middle':
            self.middle = value
            return

        if item == 'right':
            self.middle = value
            return

        services.logger.err(f'ERR bad item name: {item}')
        services.harness.abort()
