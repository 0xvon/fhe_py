from util.crypto.public_key import PublicKey


class RotationKey:
    def __init__(self, r: int, key: PublicKey):
        self.rotation = r
        self.key = key
        
    def __str__(self):
        return 'Rotation: %d\n%s' %(self.rotation, str(self.key))