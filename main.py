from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
import uvicorn
from encryption import Encryption
from typing import Dict, Any

app = FastAPI(title="Encryption API", description="HTTP API for encryption, decryption, signing, and verification", version="1.0.0")
encryption = Encryption(algorithm="base64")

class VerifyRequest(BaseModel):
    signature: str
    data: Dict[str, Any]

class SignResponse(BaseModel):
    signature: str

@app.post('/encrypt')
def encrypt_data(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Encrypt all properties at depth 1 of the input JSON payload.
    
    Example:
    Input: {"name": "John Doe", "age": 30, "contact": {"email": "john@example.com"}}
    Output: {"name": "Sm9obiBEb2U=", "age": "MzA=", "contact": "eyJlbWFpbCI6..."}
    """
    try:
        encrypted_data = encryption.encrypt(payload)
        return encrypted_data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post('/decrypt')
def decrypt_data(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Decrypt Base64 encrypted values in the JSON payload.
    Non-encrypted values remain unchanged.
    
    Example:
    Input: {"name": "Sm9obiBEb2U=", "age": "MzA=", "birth_date": "1998-11-19"}
    Output: {"name": "John Doe", "age": 30, "birth_date": "1998-11-19"}
    """
    try:
        decrypted_data = encryption.decrypt(payload)
        return decrypted_data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post('/sign', response_model=SignResponse)
def sign_data(payload: Dict[str, Any]) -> SignResponse:
    """
    Generate HMAC signature for the input JSON payload.
    The signature is computed based on the value of the JSON payload,
    so property order does not affect the signature.
    
    Example:
    Input: {"message": "Hello World", "timestamp": 1616161616}
    Output: {"signature": "a1b2c3d4e5f6g7h8i9j0..."}
    """
    try:
        signature = encryption.sign(payload)
        return SignResponse(signature=signature)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post('/verify')
def verify_signature(request: VerifyRequest) -> Response:
    """
    Verify HMAC signature for the given data.
    Returns HTTP 204 if signature is valid, HTTP 400 if invalid.
    
    Example:
    Input: {
        "signature": "a1b2c3d4e5f6g7h8i9j0...",
        "data": {"message": "Hello World", "timestamp": 1616161616}
    }
    Output: HTTP 204 (No Content) or HTTP 400 (Bad Request)
    """
    try:
        is_valid = encryption.verify(request.data, request.signature)
        if is_valid:
            return Response(status_code=204)
        else:
            return Response(status_code=400) 
    except Exception as e:
        return Response(status_code=400)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)