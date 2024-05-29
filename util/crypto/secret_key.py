from util.polynomial import Polynomial


class SecretKey:
    def __init__(self, s: Polynomial):
        self.s = s
        
    def __str__(self):
        return str(self.s)