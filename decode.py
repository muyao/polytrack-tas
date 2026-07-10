import zlib
import base64

w1_b64 = "eNpjYgABCSYGZAAAAcMAHQ=="
sw_b64 = "eNpjYmDgYmV4zMwABEwggiGGkQECABfxAVc="
ins_b64 = "eNpjZEAHAAAkAAI="
allc_b64 = "eNpjYmD4yM2wgYGBiYGhmplhMpgBBElgxg82hnYwFwBn5wSt"
allc2_b64 = "eNpjYmD4zMuQyczAxMDwnpUhnIGBhQEEHBkYljEymDCAxBU5GezAggB8WwRG"

w10_b64 = "eNoTYQABIwaGWQwMSgwMRxgYVBgYKhgYrBgY+sFkL1i2jYFBD6xGlYFhIgODEwPDEgYGUwYUAAAytAdE"
w11_b64 = "eNpVyqENgDAUANE3RZNugMBQJAmYzkRQIFDdoOMSvuuJy4lLfjIvC42dk5mHGl65meiUeDYujuhi4ANLswdo" 
w12_b64 = "eNpNxiEKgEAUQME5xlZhEWxmy2LwTms3KRhEtnhZ8SdfGF7yldkorExcdJz0NBYqI3d4MLMz8MTX8N8LlD0IdQ=="
w14_b64 = "eNpVyjEOQFAUBdGzBq1fiKBQKCwSC/ilTqmxRM/rTDG5mdziY2Kjp1LYGdJr9ig3LWfucMPFmJ+FIx2942H24wUA8QmW"

w1 = zlib.decompress(base64.b64decode(w1_b64))
sw = zlib.decompress(base64.b64decode(sw_b64))
ins = zlib.decompress(base64.b64decode(ins_b64))
allc = zlib.decompress(base64.b64decode(allc_b64))
allc2 = zlib.decompress(base64.b64decode(allc2_b64))

w10 = zlib.decompress(base64.b64decode(w10_b64))
w11 = zlib.decompress(base64.b64decode(w11_b64))
w12 = zlib.decompress(base64.b64decode(w12_b64))
w14 = zlib.decompress(base64.b64decode(w14_b64))

print("1 Tap Uncompressed:", w1.hex(" "))
print("Sw Uncompressed:", sw.hex(" "))
print("Ins Uncompressed:", ins.hex(" "))
print("Allc Uncompressed:", allc.hex(" "))
print("Allc2 Uncompressed:", allc2.hex(" "))

print("10 Taps Uncompressed:", w10.hex(" "))
print("11 Taps Uncompressed:", w11.hex(" "))
print("12 Taps Uncompressed:", w12.hex(" "))
print("14 Taps Uncompressed:", w14.hex(" "))