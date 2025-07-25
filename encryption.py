import base64
import hashlib

class Encryption:
    def __init__(self, algorithm):
        self.algorithm = algorithm
        self._secret_key = ""
    
    def encrypt(self, data):
        if self.algorithm == "base64":
            return base64.b64encode(data.encode()).decode()
        return data
    
    def decrypt(self, data):
        if self.algorithm == "base64":
            try:
                return base64.b64decode(data.encode()).decode()
            except Exception:
                raise ValueError("Invalid base64 data")
        return data
    
    def sign(self, data):
        return data
    
    def verify(self, data, signature):
        return data == signature