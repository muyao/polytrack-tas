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

"""

\x02\x00 // 2 actions
\x00\x00\x00
\x00\x18\x02
\x00\x00\x00
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00 // nullbytes


\x02\x00
\x00\n\x05
\x00\xe3\x03
\x00\x00\x00
\x00\x02\x00
\x00\x00\x00
\x00\\\x01\x00\x00\x00\x00\x00\x00\x00


\x01\x00
\x00\x00\x00
\x00\x00\x00
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00


\x02\x00\x00
\xf1\x0b\x00
\xb0\x00\x00
\x02\x00\x00
{\x03\x00
\x93\x00\x00
\x02\x00\x00
\x00\x00\x00
b\x00\x00
\x02\x00\x00
\xf8\x06\x00
\x87\x00\x00
\x00\x00\x00





eNpjYmD4zMuQyczAxMDwnpUhnIGBhQEEHBkYljEymDCAxBU5GezAggB8WwRG
Replace all _ with /, - with + for valid b64 (also add padding)
02 00 00	Length: 2 (W key, I pressed this last)
f3 0d 00	Start at frame 3571
69 03 00	Duration: 873 frames
02 00 00	Length: 2 (A or D, I can't remember which one I pressed first)
ef 05 00	Start at frame 1519
57 00 00	Duration: 87 frames
04 00 00	Length: 4 (S key, I pressed this first)
00 00 00	Start at frame 0
41 00 00	Duration: 65 frames
a6 01 00	Start at frame 422
34 00 00	Duration: 52 frames
02 00 00	Length: 2 (A or D, can't remember)
21 09 00	Start at frame 2337
3e 00 00	Duration: 62 frames
00 00 00	End here






"""