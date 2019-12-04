# Find word(s) in a subtitle file

python script to search for a string in a subtitle file,
output the in and out times of the found occurrances and
write a XML snippet to be pasted into a shotcut .mlt

## prerequisites

python3

python packages:
pandas, srt, datetime, sys, getopt, re

## usage

'find_word.py -i <inputfile> -o <outputfile> -w <word>'
If the search "word" is composed of multiple words use hyphens
