import base64
import hashlib
import hmac
import json
import os

class Encryption:
    def __init__(self, algorithm="base64"):
        self.algorithm = algorithm.lower()
        self._secret_key = os.environ.get('SECRET_KEY', 'default-secret-key-change-in-production')
    
    def encrypt(self, data):
        """Encrypt all properties at depth 1 using Base64"""
        if not isinstance(data, dict):
            return base64.b64encode(str(data).encode()).decode()
        
        result = {}
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                json_str = json.dumps(value, sort_keys=True, separators=(',', ':'))
                result[key] = base64.b64encode(json_str.encode()).decode()
            else:
                result[key] = base64.b64encode(str(value).encode()).decode()
        
        return result
    
    def decrypt(self, data):
        """Decrypt Base64 encrypted values, leaving non-encrypted values unchanged"""
        if not isinstance(data, dict):
            try:
                decoded = base64.b64decode(str(data).encode()).decode()
                try:
                    return json.loads(decoded)
                except json.JSONDecodeError:
                    return decoded
            except Exception:
                return data
        
        result = {}
        for key, value in data.items():
            if isinstance(value, str):
                try:
                    decoded = base64.b64decode(value.encode()).decode()
                    try:
                        parsed = json.loads(decoded)
                        result[key] = parsed
                    except json.JSONDecodeError:
                        try:
                            if '.' in decoded:
                                result[key] = float(decoded)
                            else:
                                result[key] = int(decoded)
                        except ValueError:
                            result[key] = decoded
                except Exception:
                    result[key] = value
            else:
                result[key] = value
        
        return result
    
    def _normalize_for_signing(self, data):
        """Convert data to a normalized string for consistent signing regardless of property order"""
        if isinstance(data, dict):
            return json.dumps(data, sort_keys=True, separators=(',', ':'))
        elif isinstance(data, list):
            return json.dumps(data, separators=(',', ':'))
        else:
            return str(data)
    
    def sign(self, data):
        """Generate HMAC signature for the given data"""
        normalized_data = self._normalize_for_signing(data)
        signature = hmac.new(
            self._secret_key.encode(),
            normalized_data.encode(),
            hashlib.sha256
        ).hexdigest()
        return signature
    
    def verify(self, data, signature):
        """Verify HMAC signature for the given data"""
        expected_signature = self.sign(data)
        return hmac.compare_digest(signature, expected_signature)