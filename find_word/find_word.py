# python script to search for a string in a subtitle file
# and output the in and out times of the found occurrances
# write a XML snippet to be pasted into a shotcut .mlt

import pandas as pd
import srt
import datetime
import sys
import getopt
import re

def main(argv):
    inputfile = ''
    outputfile = ''
    word = ''
    try:
       opts, args = getopt.getopt(argv,"hi:o:w:",["ifile=","ofile=","word="])
    except getopt.GetoptError:
      print ('find_word.py -i <inputfile> -o <outputfile> -w <word>')
      sys.exit(2)
    for opt, arg in opts:
       if opt == '-h':
          print ('find_word.py -i <inputfile> -o <outputfile> -w <word>')
          sys.exit()
       elif opt in ("-i", "--ifile"):
          inputfile = arg
       elif opt in ("-o", "--ofile"):
          outputfile = arg
       elif opt in ("-w", "--word"):
          word = arg
    print ('Reading subtitle .srt file', inputfile)
    print ('Output .XML file is', outputfile)
    print ('Search word(s) is (are)', word)
    
    subtitle = open(inputfile, "r")
    data = list(srt.parse(subtitle))
 
    cut_list = pd.DataFrame(columns=['start', 'end', 'contant'])
    xml = open(outputfile, "w") 
    for i in range(len(data)):
        if word in data[i].content:
            start = srt.timedelta_to_srt_timestamp(data[i].start)
            end = srt.timedelta_to_srt_timestamp(data[i].end)
            print(start, end)
            start = re.sub(',', '.', start)
            end = re.sub(',', '.', end)
            xml.write('''<entry producer="producer0" in="%s", out="%s" />\n''' %(start, end))
            cut_list = cut_list.append({'start': start, 'end':end, 'contant': data[i].content}, ignore_index=True)
    cut_list
    
if __name__ == "__main__":
    main(sys.argv[1:])
