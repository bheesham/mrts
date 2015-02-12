# MRTS
Magic Realm Tile Scanner

All of the data collected is in `data.json`, and does not require
running the script. Simply use a JSON parser in your language of
choice to use the data.

Known bug: some of the tiles have their names in blue which does not
get scanned. It's easy enough to add by hand, so I did. 

## Project layout
  * `data.json`: has all of the data gathered from the `MRTS.py` script.
  * `MRTS.py`: Goes through all of the `PNG` tiles and outputs data to
			`data.json`.
  * `MRCT.py`: Converts `GIF` to `PNG`.
  * `tiles/`: tiles in `GIF` and `PNG` format.

## Required libraries to `MRTS.py`
See `requirements.txt`. Each of those libraries may have their own
requirements.