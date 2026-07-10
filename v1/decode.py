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
print(rec)

# Will be final output
output = {}

# For turning delta time into absolute frames
elapsed = 0

# W actions
w_len = rec[0]
w_actions = rec[1 : w_len + 1]

# Add W actions to output
for idx, val in enumerate(w_actions):

	elapsed += val

	# Idx is even: starting frame
	if idx % 2 == 0:
		frame = elapsed

		# If frame does not exist, add frame
		if frame not in output:
			output[frame] = {}

		# For infinite keydown
		if idx == len(w_actions) - 1 and len(w_actions) % 2 != 0:
			output[frame]["w"] = -1
			continue

		# Will be changed in next iteration
		output[frame]["w"] = None

		# Skip
		continue
	
	# Duration, if index is odd
	output[frame]["w"] = val

# Reset elapsed
elapsed = 0

# D actions
d_len = rec[w_len + 1]
d_actions = rec[w_len + 2 : w_len + d_len + 2]

# Add D actions to output
for idx, val in enumerate(d_actions):

	elapsed += val

	# Idx is even: starting frame
	if idx % 2 == 0:
		frame = elapsed

		# If frame does not exist, add frame
		if frame not in output:
			output[frame] = {}

		# For infinite keydown
		if idx == len(d_actions) - 1 and len(d_actions) % 2 != 0:
			output[frame]["d"] = -1
			continue

		# Will be changed in next iteration
		output[frame]["d"] = None

		# Skip
		continue
	
	# Duration, if index is odd
	output[frame]["d"] = val

# Reset elapsed
elapsed = 0

# S actions
s_len = rec[w_len + d_len + 2]
s_actions = rec[w_len + d_len + 3 : w_len + d_len + s_len + 3]

# Add S actions to output
for idx, val in enumerate(s_actions):

	elapsed += val

	# Idx is even: starting frame
	if idx % 2 == 0:
		frame = elapsed

		# If frame does not exist, add frame
		if frame not in output:
			output[frame] = {}

		# For infinite keydown
		if idx == len(s_actions) - 1 and len(s_actions) % 2 != 0:
			output[frame]["s"] = -1
			continue

		# Will be changed in next iteration
		output[frame]["s"] = None

		# Skip
		continue
	
	# Duration, if index is odd
	output[frame]["s"] = val

# Reset elapsed
elapsed = 0

# A actions
a_len = rec[w_len + d_len + s_len + 3]
a_actions = rec[w_len + d_len + s_len + 4 : w_len + d_len + s_len + a_len + 4]

# Add A actions to output
for idx, val in enumerate(a_actions):

	elapsed += val

	# Idx is even: starting frame
	if idx % 2 == 0:
		frame = elapsed

		# If frame does not exist, add frame
		if frame not in output:
			output[frame] = {}

		# For infinite keydown
		if idx == len(a_actions) - 1 and len(a_actions) % 2 != 0:
			output[frame]["a"] = -1
			continue

		# Will be changed in next iteration
		output[frame]["a"] = None

		# Skip
		continue
	
	# Duration, if index is odd
	output[frame]["a"] = val

# Reset elapsed
elapsed = 0

# Reset actions
reset_len = rec[w_len + d_len + s_len + a_len + 4]
reset_actions = rec[w_len + d_len + s_len + a_len + 5 : w_len + d_len + s_len + a_len + reset_len + 5]

# Add reset actions to output
for idx, val in enumerate(reset_actions):

	elapsed += val

	# Idx is even: starting frame
	if idx % 2 == 0:
		frame = elapsed

		# If frame does not exist, add frame
		if frame not in output:
			output[frame] = {}

		# For infinite keydown
		if idx == len(reset_actions) - 1 and len(reset_actions) % 2 != 0:
			output[frame]["reset"] = -1
			continue

		# Will be changed in next iteration
		output[frame]["reset"] = None

		# Skip
		continue
	
	# Duration, if index is odd
	output[frame]["reset"] = val

output = {k: output[k] for k in sorted(output, key=int)}

with open(Path(__file__).resolve().parent / INSTRUCTIONS_NAME, "w") as f:
	json.dump(output, f, indent="\t")