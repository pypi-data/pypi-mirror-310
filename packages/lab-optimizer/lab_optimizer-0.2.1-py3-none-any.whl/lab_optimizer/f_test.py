import numpy as np
class f:
    @staticmethod
    def _doc():
        return "a"
    
    def __init__(self):
        self.s = 1
        
    def __str__(self):
        return "a"
    
    def __repr__(self):
        return "b"

print(f._doc())