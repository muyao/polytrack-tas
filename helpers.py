# Linear interpolation
def lerp(a, b, t):
	return a * (1 - t) + b * t

# Check if there are any automatics in instructions
def automatics_exist(instructions):

	# For each channel
	for k in ["w", "d", "s", "a", "r"]:
		channel = instructions[k]

		# For each action
		for idx, action in enumerate(channel):

			# Skip if @ not found
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