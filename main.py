import base64
import json
import os
import secrets
import subprocess
import zlib
from pathlib import Path

if __name__ != "__main__":
	exit(0)

SH_PATH = "/bin/bash"
USER_AGENT = "Mozilla/5.0"
NICKNAME = "XxXxxxXxX"
CAR_STYLE = "AAAAAC13Fv___xMTE2ZmZg"
TRACK_ID = "95e4bf5c2a76b49ad1ce0f7fd9d6ca777a09aaf6492f9a7415afde3427a8ac66"
FRAMES = "3282"
ONLY_VERIFIED = "false"

# Load instructions
with open(Path(__file__).resolve().parent / "instructions.json") as f:
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
			raise Exception(f"Unknown key: {k} in frame {frame}. See instructions.json.")

		# Store instruction, convert to little-endian
		wasd[k].append(int(frame).to_bytes(3, byteorder="little"))
		wasd[k].append(int(d).to_bytes(3, byteorder="little"))

# First add all W
rec += len(wasd["w"]).to_bytes(3, byteorder="little")
for v in wasd["w"]:
	rec += v

# Then all A
rec += len(wasd["a"]).to_bytes(3, byteorder="little")
for v in wasd["a"]:
	rec += v

# S
rec += len(wasd["s"]).to_bytes(3, byteorder="little")
for v in wasd["s"]:
	rec += v

# D
rec += len(wasd["d"]).to_bytes(3, byteorder="little")
for v in wasd["d"]:
	rec += v

# Add three null bytes at the end
rec += b"\x00\x00\x00"

# Compress with zlib
rec = zlib.compress(rec, level=9)

# Convert to Base64
rec = base64.b64encode(rec).decode('utf-8')

# Polytrack uses - and _ instead of + and /
rec = rec.replace("+", "-").replace("/", "_").replace("=", "")

# Generate the shellscript
with open("/tmp/polyhax.post.sh", "w") as f:
	f.write(f"#!{SH_PATH}\n")
	f.write("curl 'https://vps.kodub.com/v6/leaderboard' ")
	f.write("-H 'Content-Type: application/x-www-form-urlencoded' ")
	f.write("-H 'Origin: https://app-polytrack.kodub.com' ")
	f.write("-H 'Referer: https://app-polytrack.kodub.com/' ")
	f.write(f"-H 'User-Agent: {USER_AGENT}' ")
	f.write("--data-raw 'version=0.6.2&")
	f.write(f"userToken={secrets.token_hex(32)}&")
	f.write(f"nickname={NICKNAME}&")
	f.write(f"carStyle={CAR_STYLE}&")
	f.write(f"trackId={TRACK_ID}&")
	f.write(f"frames={FRAMES}&")
	f.write(f"recording={rec}&")
	f.write(f"onlyVerified={ONLY_VERIFIED}'")

# Give file execution permissions
os.chmod("/tmp/polyhax.post.sh", 0o744)

# Execute shellscript
subprocess.run(["/tmp/polyhax.post.sh"])

# Clean up
os.remove("/tmp/polyhax.post.sh")