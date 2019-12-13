import argparse
import ffmpeg
import pandas

def main():
    """Automatically cutting a video using ffmpeg."""


    parser = argparse.ArgumentParser(prog="cutter",
                                     description="Cutting videos using a decision list and FFmpeg")

    parser.add_argument("list", help="path to cut list")
    parser.add_argument("input", help="input video file")
    #parser.add_argument("basename", help="basename for the scenes")
    parser.add_argument("-v",
                        "--verbose",
                        action='store_true',
                        help="verbose mode")

    args = parser.parse_args()

    stream = 0
    output = 'scene'
    video_list = []
    audio_list = []
    merge_list = []

    raw = ffmpeg.input(args.input)
    cut_list = pandas.read_pickle(args.list)

    print(cut_list)

    for i, scene in cut_list.iterrows():
        start = cut_list.start[i]
        end = cut_list.end[i]

        if args.verbose:
            print('   Start %s, End %s' % (start, end))

        audio = (
            raw
            .filter_('atrim', start=start, end=end)
            .filter_('asetpts', 'PTS-STARTPTS')
        )

        video = ffmpeg.trim(raw, start=start, end=end)
        video = video.setpts('PTS-STARTPTS')

        stream = ffmpeg.concat(video, audio, v=1, a=1)
        stream = ffmpeg.output(stream, output + str(i) + '.mp4')
        stream.run()

if __name__ == "__main__":
    main()
