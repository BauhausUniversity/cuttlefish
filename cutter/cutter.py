import argparse
import ffmpeg
import pandas
<<<<<<< HEAD
import re
from timecode import Timecode
from scenedetect.video_manager import VideoManager
=======
>>>>>>> 85f55d082d85585ec00aae764c96680c0ba358c8

def main():
    """Automatically cutting a video using ffmpeg."""


    parser = argparse.ArgumentParser(prog="cutter",
                                     description="Cutting videos using a decision list and FFmpeg")

    parser.add_argument("list", help="path to cut list")
    parser.add_argument("input", help="input video file")
<<<<<<< HEAD
    parser.add_argument("-t",
                        "--tolerance",
                        action="store",
                        default=0,
                        help="number of frames added")
=======
>>>>>>> 85f55d082d85585ec00aae764c96680c0ba358c8
    #parser.add_argument("basename", help="basename for the scenes")
    parser.add_argument("-v",
                        "--verbose",
                        action='store_true',
                        help="verbose mode")

    args = parser.parse_args()

    stream = 0
    output = 'scene'

    video_manager = VideoManager([args.input])
    fps = video_manager.get_framerate()
    # tolerance = Timecode(fps, frames=int(args.tolerance)).frames_to_tc
    tolerance = int(args.tolerance)

    if args.verbose:
        print("FPS: %d" % (fps))
        print(tolerance)

    raw = ffmpeg.input(args.input)
    cut_list = pandas.read_pickle(args.list)

    for i, scene in cut_list.iterrows():
        start = re.sub(',', '.', cut_list.start[i])
        end = re.sub(',', '.', cut_list.end[i])

        print("%s %s" % (start, end))

        start = Timecode(fps, start) - tolerance
        start.set_fractional(True)

        end = Timecode(fps, end) + tolerance
        end.set_fractional(True)

        print("%s %s" % (start, end))

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
