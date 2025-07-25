from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from encryption import Encryption

app = FastAPI()
encryption = Encryption(algorithm="base64")

# Request models
class EncryptRequest(BaseModel):
    data: dict

class DecryptRequest(BaseModel):
    encrypted_data: dict

class SignRequest(BaseModel):
    data: dict

class VerifyRequest(BaseModel):
    data: str
    signature: str

# Response models
class EncryptResponse(BaseModel):
    encrypted_data: str

class DecryptResponse(BaseModel):
    decrypted_data: str

class SignResponse(BaseModel):
    signature: str
    data: str

class VerifyResponse(BaseModel):
    is_valid: bool

@app.post('/encrypt', response_model=EncryptResponse)
def encrypt_data(request: EncryptRequest):
    try:
        encrypted_data = encryption.encrypt(request.data)
        return EncryptResponse(encrypted_data=encrypted_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post('/decrypt', response_model=DecryptResponse)
def decrypt_data(request: DecryptRequest):
    try:
        decrypted_data = encryption.decrypt(request.encrypted_data)
        return DecryptResponse(decrypted_data=decrypted_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post('/sign', response_model=SignResponse)
def sign_data(request: SignRequest):
    try:
        signature = encryption.sign(request.data)
        return SignResponse(signature=signature, data=request.data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post('/verify', response_model=VerifyResponse)
def verify_signature(request: VerifyRequest):
    try:
        is_valid = encryption.verify(request.data, request.signature)
        return VerifyResponse(is_valid=is_valid)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)