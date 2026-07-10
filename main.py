import base64
import json
import requests
import secrets
import zlib
from config import *
from pathlib import Path

if __name__ != "__main__":
	exit(0)

# Load instructions
with open(Path(__file__).resolve().parent / INSTRUCTIONS_NAME) as f:
	instructions = json.load(f)

# Temporary storage
wasd = {
	"w": [],
	"a": [],
	"s": [],
	"d": []
}

# Recording. Will get appended from wasd in order W, A, S, D
rec = b""

# Iterate through each frame (Frame as in one screen refresh)
for frame in instructions:
	instruction = instructions[frame]

	# For each action of an instruction
	for k in instruction:
		d = instruction[k]

		# If key is not WASD then throw error
		if k not in wasd:
			raise Exception(f"Unknown key: {k} in frame {frame}. See {INSTRUCTIONS_NAME}.")

		# Store instruction, convert to little-endian
		wasd[k].append(int(frame).to_bytes(3, byteorder="little"))
		wasd[k].append(int(d).to_bytes(3, byteorder="little"))

# First add all W
rec += len(wasd["w"]).to_bytes(3, byteorder="little")
for v in wasd["w"]:
	rec += v

# Then all D
rec += len(wasd["d"]).to_bytes(3, byteorder="little")
for v in wasd["d"]:
	rec += v

# S
rec += len(wasd["s"]).to_bytes(3, byteorder="little")
for v in wasd["s"]:
	rec += v

# A
rec += len(wasd["a"]).to_bytes(3, byteorder="little")
for v in wasd["a"]:
	rec += v

# Add three null bytes at the end
rec += b"\x00\x00\x00"

# Compress with zlib
rec = zlib.compress(rec, level=9)

# Convert to Base64
rec = base64.b64encode(rec).decode("utf-8")

# Polytrack uses - and _ instead of + and /
rec = rec.replace("+", "-").replace("/", "_").replace("=", "")

print(requests.post(
	"https://vps.kodub.com/v6/leaderboard",
	headers={
		"Content-Type": "application/x-www-form-urlencoded",
		"Origin": "https://app-polytrack.kodub.com",
		"Referer": "https://app-polytrack.kodub.com/",
		"User-Agent": USER_AGENT
	},
	data={
		"version": POLYTRACK_VERSION,
		"userToken": secrets.token_hex(32),
		"nickname": NICKNAME,
		"carStyle": CAR_STYLE,
		"trackId": TRACK_ID,
		"frames": FRAMES,
		"recording": rec,
		"onlyVerified": ONLY_VERIFIED
	}
).text)