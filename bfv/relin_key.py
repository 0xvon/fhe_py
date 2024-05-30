class BFVRelinKey:
    def __init__(self, base, keys):
        self.base = base
        self.keys = keys
        
    def __str__(self):
        """Represents RelinKey as a string.

        Returns:
            A string which represents the RelinKey.
        """
        return 'Base: ' + str(self.base) + '\n' + str(self.keys)