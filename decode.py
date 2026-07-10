import base64
import json
import zlib
from config import *
from pathlib import Path

if __name__ != "__main__":
	exit(0)

# Add padding
rec = DECODE_RECORDING + "=" * (-len(DECODE_RECORDING) % 4)

# Decode base64
rec = base64.urlsafe_b64decode(rec)

# Decompress with zlib
rec = zlib.decompress(rec)

# Turn rec into a list. 3 bytes per group
rec = [int.from_bytes(rec[i : i + 3], byteorder="little") for i in range(0, len(rec), 3)]

# Stringify
rec = [str(i) for i in rec]

# This will be the output
instructions = {
	"instructions_v2": {
		"w": None,
		"a": None,
		"s": None,
		"d": None,
		"reset": None
	}
}

# Iterate through all channels
for k in ["w", "d", "s", "a", "reset"]:

	# Take the slice for the channel and delete
	actions = rec[1 : int(rec[0]) + 1]
	del rec[0 : int(rec[0]) + 1]

	# Add to output, in this format: xxx-yyy
	instructions["instructions_v2"][k] = ["-".join(actions[i : i + 2]) for i in range(0, len(actions), 2)]

# Write to output json
with open(Path(__file__).resolve().parent / INSTRUCTIONS_NAME, "w") as f:
	instructions = json.dump(instructions, f, indent="\t")