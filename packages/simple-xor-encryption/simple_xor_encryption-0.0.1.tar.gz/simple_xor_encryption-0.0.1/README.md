# xor_encryption
*yet another useless and random package*
## exemple
```python
from xor_encryption import xor

message = "random test".encode()
key = "SsJflOuZt7g".encode()  # key *must* be the same length as the message

encrypted_message = xor(message, key)
decrypted_message = xor(encrypted_message, key)
print(message == decrypted_message)
```