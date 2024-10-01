import base64

# String to be encoded
string_to_encode = "password"

# Encode the string to base64
encoded_string = base64.b64encode(string_to_encode.encode('utf-8'))
# encoded_string = "YVoxbXV0aA=="
# Decode the encoded string back to original
decoded_string = base64.b64decode(encoded_string).decode('utf-8')

print("Original string:", string_to_encode)
print("Encoded string:", encoded_string.decode('utf-8'))
print("Decoded string:", decoded_string)