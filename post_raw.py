import requests
import secrets
from config import *

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
			"nickname": NICKNAME,
			"carStyle": CAR_STYLE,
			"trackId": TRACK_ID,
			"frames": FRAMES,
			"recording": DECODE_RECORDING,
			"onlyVerified": ONLY_VERIFIED
		}
	).text
)