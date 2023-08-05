# simple_xor_encryption
*yet another useless and random package*
## exemple
```python
from simple_xor_encryption import xor

message = "random test".encode()
key = "SsJt7g".encode()  # key length does not have to match data length

encrypted_message = xor(message, key)
decrypted_message = xor(encrypted_message, key)
print(message == decrypted_message)
```