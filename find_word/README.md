# Find word(s) in a subtitle file 📑

python script to search for a string in a subtitle file,
output the in and out times of the found occurrances and
write a XML snippet to be pasted into a shotcut .mlt

## prerequisites

`python3`

python packages:
`argparse`, `re`, `srt`, `ffmpeg`, `pandas`

## usage

`find_word [-h] [-i INPUTFILE] [-o OUTPUTFILE] [-w WORD] [-c CUT CUT] [-v]`

If the search “word” is composed of multiple words use hyphens

use the flag `-v` or `--verbose` for verbose output.
