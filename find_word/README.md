# Find word(s) in a subtitle file 📑

python script to search for a string in a subtitle file,
output the in and out times of the found occurrances and
write a XML snippet to be pasted into a shotcut .mlt

## prerequisites

`python3`

python packages:
`argparse`, `re`, `srt`, `ffmpeg`, `pandas`

## setup

In order to install the dependencies automatically, execute:

`pip3 install -r requirements.txt`

## usage

`python3 find_word.py [-h] [-i INPUTFILE] [-o OUTPUTFILE] [-w WORD] [-c] [-v]`

If the search “word” is composed of multiple words use hyphens

If flag `-c` is used, the list of scenes will be exported to a pickle file.

use the flag `-v` or `--verbose` for verbose output.

The output .xml file contains a snippet of .xml code which can be pasted into a shotcut .mlt file. For this make a new Shotcut document and put the source video in the playlist. Then save and close the document and use a text editor to replace the playlist part with the snippet from this python script.
