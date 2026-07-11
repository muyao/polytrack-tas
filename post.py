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
	instructions = json.load(f)["instructions_v2"]

# Will be the output
rec = []

# For each channel
for k in ["w", "d", "s", "a", "r"]:
	channel = instructions[k]

	# All the actions of current channel
	actions = []

	# For each action
	for action in channel:

		# Comments
		if action.startswith(":"):
			continue

		# Split xxx-yyy into [xxx, yyy]
		action_pair = action.split("-")

		# For spam macros, like !900-45-45-10
		if action.startswith("!"):

			# Repeat last bit times
			for s in range(int(action_pair[3])):

				# Add DTs to actions
				actions.append(action_pair[1])
				actions.append(action_pair[2])
				
			continue

		# Concat to actions
		actions += action_pair

	# Add to output
	rec.append(len(actions))
	rec += actions

# Intify rec
rec = [int(i) for i in rec]

# Bytify rec
rec = [i.to_bytes(3, byteorder="little") for i in rec]

# Turn rec into string (rec_s)
rec_s = b""
for btr in rec:
	rec_s += btr

# Compress with zlib
rec = zlib.compress(rec_s, level=9)

# Convert to Base64
rec = base64.urlsafe_b64encode(rec).decode("utf-8")

# Remove the padding
rec = rec.rstrip("=")

if RANDOMISE_NICKNAME:
	nickname = secrets.token_hex(16)
else:
	nickname = NICKNAME

print(
	requests.post(
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
			"nickname": nickname,
			"carStyle": CAR_STYLE,
			"trackId": TRACK_ID,
			"frames": FRAMES,
			"recording": rec,
			"onlyVerified": ONLY_VERIFIED
		}
	).text
)