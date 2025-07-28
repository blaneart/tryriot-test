# Encryption API

HTTP API with 4 endpoints for encryption, decryption, signing, and verification.

## Quick Start

```bash
pip install -r requirements.txt
python main.py
```

API available at `http://localhost:8000`

## Usage Examples

### Encrypt
```bash
curl -X POST "http://localhost:8000/encrypt" \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "age": 30, "contact": {"email": "john@example.com"}}'
```

### Decrypt
```bash
curl -X POST "http://localhost:8000/decrypt" \
  -H "Content-Type: application/json" \
  -d '{"name": "Sm9obiBEb2U=", "age": "MzA=", "contact": "eyJlbWFpbCI6ImpvaG5AZXhhbXBsZS5jb20ifQ=="}'
```

### Sign
```bash
curl -X POST "http://localhost:8000/sign" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello World", "timestamp": 1616161616}'
```

### Verify
```bash
curl -X POST "http://localhost:8000/verify" \
  -H "Content-Type: application/json" \
  -d '{"signature": "663e4f688b291dee74962c0d79708d054e6db1c1ea5d2802adc72b27b659bcca", "data": {"message": "Hello World", "timestamp": 1616161616}}'
```

Valid signature returns HTTP 204, invalid returns HTTP 400.