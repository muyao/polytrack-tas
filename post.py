import base64
import json
import pyperclip
import requests
import secrets
import time
import zlib
from config import *
from helpers import *
from pathlib import Path

if __name__ != "__main__":
	exit(0)

# Pack everything into a function, for autos that will post multiple times
def post(instructions, t):

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

			# Auto
			if "@" in action:

				# Only for the one with @ in it
				for idx, ac_sing_p in enumerate(action_pair):
					if "@" not in ac_sing_p:
						continue

					# @800.1000 -> min_max = ["800", "1000"]
					min_max = ac_sing_p.replace("@", "").replace("!", "")
					min_max = min_max.split(".")
					action_pair[idx] = str(
						round(
							lerp(
								int(min_max[0]),
								int(min_max[1]),
								t
							)
						)
					)

			# For spam macros, like !900-45-45-10
			if action.startswith("!"):

				# Repeat last bit times
				for s in range(int(action_pair[3])):

					# Add DTs to actions
					if s == 0:
						actions.append(action_pair[0].replace("!", ""))
					else:
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

	# User token
	if RANDOMISE_USER_TOKEN:
		user_token = secrets.token_hex(32)
	else:
		user_token = USER_TOKEN

	# Nickname
	if RANDOMISE_NICKNAME:
		nickname = secrets.token_hex(16)
	else:
		nickname = NICKNAME

	# Print recording
	print(rec)

	# Generate Javascript to paste into console
	js = (
		f"((r=JSON.parse(localStorage.getItem(\"{LOCALSTORAGE_KEY}\")))=>{{if("
		f"r===null){{return \"Go to https://app-polytrack.kodub.com/"
		f"{POLYTRACK_VERSION}/! If you already are there, set a record on that"
		f" track first.\"}}r.recording=\"{rec}\";localStorage.setItem(\""
		f"{LOCALSTORAGE_KEY}\",JSON.stringify(r));return localStorage}})()"
	)
	# Ignore the abomination above
	pyperclip.copy(js)

	# Don't post if IS_TESTING	
	if IS_TESTING:
		return

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
				"userToken": user_token,
				"nickname": nickname,
				"carStyle": CAR_STYLE,
				"trackId": TRACK_ID,
				"frames": FRAMES,
				"recording": rec,
				"onlyVerified": ONLY_VERIFIED
			}
		).text
	)

# Find location of auto
def find_auto(instructions):

	# For each channel
	for k in ["w", "d", "s", "a", "r"]:
		channel = instructions[k]

		# For each action
		for idx, action in enumerate(channel):

			# Skip to next iteration if @ not found
			if "@" not in action:
				continue

			# Skip comments
			if action.startswith(":"):
				continue

			# Error
			if "." not in action:
				raise Exception()

			# Return True if an automatic is found 
			return True
	
	# Otherwise, return False
	return False

# Load instructions
with open(Path(__file__).resolve().parent / INSTRUCTIONS_NAME) as f:
	instrv2 = json.load(f)["instructions_v2"]

# Location of automatic
auto_found = find_auto(instrv2)

# If there is no automatic, just post once
if not auto_found:
	post(instrv2, None)
	exit(0)

# Otherwise, repeat AUTO_AMOUNT with t starting at 0, ending at 1
for t in range(AUTO_AMOUNT):
	post(instrv2, t / (AUTO_AMOUNT - 1))

	# Skip wait if is testing, can't be 429ed
	if IS_TESTING:
		continue

	# Wait 1s to avoid rate limit
	time.sleep(1)