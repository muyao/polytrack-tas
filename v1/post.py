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
	"d": [],
	"reset": []
}

# For converting absolute times to DT
prev = {
	"w": 0,
	"a": 0,
	"s": 0,
	"d": 0,
	"reset": 0
}

# Recording. Will get appended from wasd in order W, A, S, D, Reset
rec = b""

# Iterate through each frame (Frame as in one screen refresh)
for frame in instructions:
	instruction = instructions[frame]

	# For each action of an instruction
	for k in instruction:
		d = instruction[k]

		# If key is not WASD then throw error
		if k not in wasd:
			raise Exception(f"Unknown key: {k} in frame {frame}.")

		# Store instruction, convert to little-endian
		wasd[k].append((int(frame) - prev[k]).to_bytes(3, byteorder="little"))

		# Only add a duration if duration is > 0. Otherwise, duration is infinite
		if int(d) >= 0:
			wasd[k].append(int(d).to_bytes(3, byteorder="little"))
		
		# Set previous
		prev[k] = int(frame) + d

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

# Reset
rec += len(wasd["reset"]).to_bytes(3, byteorder="little")
for v in wasd["reset"]:
	rec += v

# Compress with zlib
rec = zlib.compress(rec, level=9)

# Convert to Base64
rec = base64.urlsafe_b64encode(rec).decode("utf-8")

# Remove the padding
rec = rec.rstrip("=")

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