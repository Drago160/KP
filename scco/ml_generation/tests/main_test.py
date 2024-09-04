import base64

my_text = "My plain text with !@#$%%&"

# Encode
byte_encode = my_text.encode('utf-8')
b64_bytes = base64.b64encode(byte_encode)
b64_string = b64_bytes.decode('utf-8')
print(b64_string)

# Decode
byte_encode = b64_string.encode('utf-8')
my_text_b64_decode = base64.b64decode(byte_encode)
my_text_decode = my_text_b64_decode.decode('utf-8')
print(my_text_decode)
