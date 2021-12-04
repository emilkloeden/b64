from b64 import encode, decode

input_ = b"test"
expected = "dGVzdA=="
    
encoded = encode(input_)
decoded = decode(encoded)
print(encoded)
print(decoded)