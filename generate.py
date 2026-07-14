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

# Pack everything into a function because automatics (@xxx.yyy) will generate
# multiple times
def generate(instructions, t):

	# Will be the output
	rec = []

	# For each channel
	for k in ["w", "d", "s", "a", "r"]:
		channel = instructions[k]

		# All the actions of current channel
		actions = []

		# For each action
		for action in channel:

			# Skip comments
			if action.startswith(":"):
				continue

			# Split xxx-yyy into [xxx, yyy]
			action_pair = action.split("-")

			# Automatics
			if "@" in action:

				# Only for the segment with @ in it
				for idx, ac_sing_p in enumerate(action_pair):

					# Skip segments without @
					if "@" not in ac_sing_p:
						continue

					# For segments with @
					# Example: @800.1000 -> min_max = ["800", "1000"]
					min_max = ac_sing_p.replace("@", "").replace("!", "")
					min_max = min_max.split(".")

					# Interpolate from min to max. t=0, min. t=1, max, then
					# round and stringify
					interpolated = lerp(int(min_max[0]), int(min_max[1]), t)
					action_pair[idx] = str(round(interpolated))

			# For simple key presses
			if not action.startswith("!"):
				
				# Concat to actions
				actions += action_pair

				continue

			# Otherwise if it is a spam macro like !900-45-50-20
			# Repeat in example above 20 times, in other examples the number at
			# the end
			for s in range(int(action_pair[3])):

				# Add DTs and durations to actions
				# If it is the first iteration, use (in the example above) 900 
				# instead of 45. Otherwise, use 45
				if s == 0:
					actions.append(action_pair[0].replace("!", ""))
				else:
					actions.append(action_pair[1])
				actions.append(action_pair[2])

		# Append to output
		rec.append(len(actions))
		rec += actions

	# Intify, binarify, stringify
	rec = [int(i) for i in rec]
	rec = [i.to_bytes(3, byteorder="little") for i in rec]
	rec_s = b""
	for btr in rec:
		rec_s += btr

	# Compress with zlib, convert to base64, remove padding
	rec = zlib.compress(rec_s, level=9)
	rec = base64.urlsafe_b64encode(rec).decode("utf-8")
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
	# Copy abomination above to clipboard
	pyperclip.copy(js)

	# Don't post if IS_TESTING	
	if IS_TESTING:
		return

	# Otherwise, post to leaderboards
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

# Load instructions
with open(Path(__file__).resolve().parent / INSTRUCTIONS_NAME) as f:
	instrv2 = json.load(f)["instructions_v2"]

# If there is no automatic, just post once
if not automatics_exist(instrv2):
	generate(instrv2, None)
	exit(0)

# Otherwise, repeat AUTO_AMOUNT with t starting at 0, ending at 1
for t in range(AUTO_AMOUNT):
	generate(instrv2, t / (AUTO_AMOUNT - 1))

	# Only wait 1s if not testing
	if not IS_TESTING:
		time.sleep(1)