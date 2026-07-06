import zlib
import base64

w11_b64 = "eNpVyqENgDAUANE3RZNugMBQJAmYzkRQIFDdoOMSvuuJy4lLfjIvC42dk5mHGl65meiUeDYujuhi4ANLswdo" 
w12_b64 = "eNpNxiEKgEAUQME5xlZhEWxmy2LwTms3KRhEtnhZ8SdfGF7yldkorExcdJz0NBYqI3d4MLMz8MTX8N8LlD0IdQ"

print("11 Taps Uncompressed:", zlib.decompress(base64.b64decode(w11_b64)))
print("12 Taps Uncompressed:", zlib.decompress(base64.b64decode(w12_b64)))