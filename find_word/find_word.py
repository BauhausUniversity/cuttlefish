"""
python script to search for a string in a subtitle file
and output the in and out times of the found occurrances
write a XML snippet to be pasted into a shotcut .mlt
"""

import argparse
import re
import srt
import ffmpeg
import pandas

CRED = '\033[91m'
CEND = '\033[0m'

def main():
    """Parsing arguments and generating an XML file."""
    parser = argparse.ArgumentParser(prog="find_word",
                                     description="Searching for strings in a subtitle file and generating an edit decision list")

    parser.add_argument("-i", "--inputfile", help="input .srt file", required=True)
    parser.add_argument("-o", "--outputfile", help="output .xml file")
    parser.add_argument("-w", "--word", help="search for word(s)", required=True)
#    parser.add_argument("-e", "--extend", help="extend clip by (use negative number to shorten)")
    parser.add_argument("-c",
                        "--cut",
                        action="store",
                        nargs=2,
                        help="Automatically cutting the video file. (input video file, output video file)")
    parser.add_argument("-v", "--verbose", action='store_true', help="verbose mode")

    args = parser.parse_args()

    # Verbose mode
    if args.verbose:
        print('Reading subtitle .srt file', CRED + args.inputfile + CEND)
        if args.outputfile is not None:
            print('Output .XML file is', CRED + args.outputfile + CEND)
        print('Search word(s) is/are', CRED + args.word + CEND)
        if args.cut is not None:
            print(args.cut[0])
            print(args.cut[1])

    subtitle = open(args.inputfile, "r")
    data = list(srt.parse(subtitle))

    cut_list = pandas.DataFrame(columns=['start', 'end', 'content'])
    if args.outputfile is not None:
        xml = open(args.outputfile, "w")

    for i in range(len(data)):
        if args.word in data[i].content:
            start = srt.timedelta_to_srt_timestamp(data[i].start)
            end = srt.timedelta_to_srt_timestamp(data[i].end)

            # Verbose mode
            if args.verbose:
                print(start, end)
            if args.outputfile is not None:
                start = re.sub(',', '.', start)
                end = re.sub(',', '.', end)
                xml.write('''<entry producer="producer0" in="%s" out="%s" />\n''' %(start, end))
                cut_list = cut_list.append({'start': start,
                                        'end':end,
                                        'content': data[i].content
                                        },
                                        ignore_index=True)

    if args.cut is not None:
        cut(args.cut[0], args.cut[1], cut_list, args.verbose)

def cut(vinput, voutput, cuts, verbose):
    """Automatically cutting a video using ffmpeg."""
    stream = 0
    video_list = []
    audio_list = []
    merge_list = []
    raw = ffmpeg.input(vinput)

    for i, scene in enumerate(cuts):
        start = cuts.start[i]
        end = cuts.end[i]

        if verbose:
            print('   Start %s, End %s' % (start, end))

        audio = (
            raw
            .filter_('atrim', start=start, end=end)
            .filter_('asetpts', 'PTS-STARTPTS')
        )

        video = ffmpeg.trim(raw, start=start, end=end)
        video = video.setpts('PTS-STARTPTS')

        video_list.append(video)
        audio_list.append(audio)

    for i in range(len(video_list)):
        merge_list.append(video_list[i])
        merge_list.append(audio_list[i])

    stream = ffmpeg.concat(*merge_list, v=1, a=1)
    stream = ffmpeg.output(stream, voutput)
    stream.run()

if __name__ == "__main__":
    main()
