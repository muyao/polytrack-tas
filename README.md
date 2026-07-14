# PolyTrack TAS

## Features

* **Post recordings directly to PolyTrack:** By running `post.py`, it converts your run to a PolyTrack recording and uploads to the leaderboards.

* **Fully customisable:** By changing `config.py`, you can change the car's style, the nickname and more.

* **Decode recordings to JSON:** By running `deode.py`, you can convert the recording specified inside `config.py` back to a JSON

## Requirements

* See `requirements.txt`
* `pip install pyperclip`
* `pip install requests`

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/muyao/polytrack-tas.git
   ```

2. **Navigate to the project directory:**
   ```bash
   cd polytrack-tas
   ```

3. **Install requirement:**
   ```bash
   pip install pyperclip
   pip install requests
   ```

## Usage

### Making a TAS run

1. Make an `instructions.json`. Paste this inside:
   ```json
   {
      "instructions_v2": {
          "w": [],
          "a": [],
          "s": [],
          "d": [],
          "r": []
      }
   }
   ```

2. Put the track ID inside `config.py`. (You can find the track ID by going into the network tab of the debug console on [PolyTrack](https://www.kodub.com/apps/polytrack), then opening a track. There should be a get request for the leaderboards.)

3. Edit `instructions.json`:

* There are instructions for each key
* Example: Press W for 500 frames, then release:
   ```json
   "w": [
       "0-500"
   ]
   ```
* Example: Press S for 300 frames, release for 200 frames, press for 400 frames:
   ```json
   "s": [
       "0-300",
       "200-400"
   ]
   ```
* Example: Press W and S for the same time
   ```json
   "w": [
       "0"
   ],
   ...
   "s": [
       "0"
   ]
   ```
* Syntax for simple keypresses:
   ```plaintext
   <dt>-[duration]
   ```
   If the duration is left away (see example 3), the key will remain pressed
* For multiple keydowns and keyups in a row, like spamming the D key, there is different syntax:
   ```json
   "d": [
       "!0-45-60-10"
   ]
   ```
   This example presses the D key 10 times for 60 frames with 45 frames in between starting from frame 0.
* Syntax:
   ```plaintext
   !<start>-<dt>-<duration>-<amount>
   ```
* To test multiple paths, use an `@`:
   ```json
   "w": [
       "0"
   ],
   ...
   "d": [
       "@200.400-250"
   ]
   ```
   This tests 4 values between 200 and 400 (200, 267, 333, 400) and sends 4 recordings to the leaderboards. You can then manually review them and check which one is the fastest.

4. Run `post.py`

### Decoding

* You can specify a recording with `DECODE_RECORDING` in `config.py`. Then, running `decode.py` puts the decoded json inside `instructions.json`.

### Configurations

* `NICKNAME`: The nickname that will show up in the leaderboards
* `RANDOMISE_NICKNAME`: If set to `True`, will turn nickname into random gibberish
* `USER_TOKEN`: Who you are
* `RANDOMISE_USER_TOKEN`: If set to `True`, will anonymise you
* `TRACK_ID`: The ID of the track
* `FRAMES`: The length that will be uploaded. 1000 frames is 1 second.
* `AUTO_AMOUNT`: How many requests `@` will send.
* `CAR_STYLE`: The car's style
* `INSTRUCTIONS_NAME`: The file name of the instruction json.
* `DECODE_RECORDING`: The recording that you want to decode using `decode.py`
* `USER_AGENT`: The header for the post request when running `post.py`
* `ONLY_VERIFIED`: I actually don't know myself what this does. Just leave this in `false`. If it doesn't work, do `true`
* `POLYTRACK_VERSION`: The version of PolyTrack.

### Examples

* Example `instruction.json` TAS runs are in the `runs/` directory.
* `example_instructions.json` and `example_config.py` are in `examples/` directory. To use them, move them out and remove the `example_` bit.

## Contributing

Contributions are what make the open-source community such an amazing place. Any contributions you make are greatly appreciated.

## License

Distributed under the GPLv3 License. See `LICENSE` for more information.

---

*v2.4.1*

*Tue, 14 Jul 2026 09:02:51 GMT*