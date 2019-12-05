# python script to search for a string in a subtitle file
# and output the in and out times of the found occurrances
# write a XML snippet to be pasted into a shotcut .mlt

import pandas as pd
import srt
import datetime
import sys
import argparse
import re

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--inputfile", help="Input file")
    parser.add_argument("-o", "--outputfile", help="Output file")
    parser.add_argument("-w", "--word", help="Word")
    parser.add_argument("-v", "--verbose", action='store_true', help="Verbose mode")

    args = parser.parse_args()

    if args.verbose is True:
        print ('Reading subtitle .srt file', args.inputfile)
        print ('Output .XML file is', args.outputfile)
        print ('Search word(s) is/are', args.word)
    
    subtitle = open(args.inputfile, "r")
    data = list(srt.parse(subtitle))
 
    cut_list = pd.DataFrame(columns=['start', 'end', 'contant'])
    xml = open(args.outputfile, "w") 
    for i in range(len(data)):
        if args.word in data[i].content:
            start = srt.timedelta_to_srt_timestamp(data[i].start)
            end = srt.timedelta_to_srt_timestamp(data[i].end)
            if args.verbose is True:
                print(start, end)
            start = re.sub(',', '.', start)
            end = re.sub(',', '.', end)
            xml.write('''<entry producer="producer0" in="%s", out="%s" />\n''' %(start, end))
            cut_list = cut_list.append({'start': start, 'end':end, 'contant': data[i].content}, ignore_index=True)
    cut_list
 
if __name__ == "__main__":
    main()
