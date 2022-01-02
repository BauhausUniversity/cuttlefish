import os
import sys, csv
import random

import scenedetect
from scenedetect.video_manager import VideoManager
from scenedetect.scene_manager import SceneManager
from scenedetect.frame_timecode import FrameTimecode
from scenedetect.stats_manager import StatsManager
from scenedetect.detectors import ContentDetector

import ffmpeg

STATS_FILE_PATH = 'stats.csv'

def main():
    
    for root, dirs, files in os.walk('material'):
        for file in files:
            file = os.path.join(root, file)

            video_manager = VideoManager([file])
            stats_manager = StatsManager()
            scene_manager = SceneManager(stats_manager)
            scene_manager.add_detector(ContentDetector())
            base_timecode = video_manager.get_base_timecode()
            end_timecode = video_manager.get_duration()

            start_time = base_timecode
            end_time = end_timecode[2]

            video_manager.set_duration(start_time=start_time, end_time=end_time)
            video_manager.set_downscale_factor()
            video_manager.start()
            scene_manager.detect_scenes(frame_source=video_manager)

            scene_list = scene_manager.get_scene_list(base_timecode)

            if stats_manager.is_save_required():
                with open(STATS_FILE_PATH, 'w') as stats_file:
                    stats_manager.save_to_csv(stats_file, base_timecode)


            print('List of scenes obtained:')
            for i, scene in enumerate(scene_list):
                print('    Scene %2d: Start %s / Frame %d, End %s / Frame %d' % (
                    i+1,
                    scene[0].get_timecode(), scene[0].get_frames(),
                    scene[1].get_timecode(), scene[1].get_frames(),))

                raw = ffmpeg.input(file)

                start = scene[0].get_timecode()
                end = scene[1].get_timecode()

                audio = (
                    raw
                    .filter_('atrim', start=start, end=end)
                    .filter_('asetpts', 'PTS-STARTPTS')
                )

                raw = ffmpeg.trim(raw, start=start, end=end)
                raw = raw.setpts('PTS-STARTPTS')

                joined = ffmpeg.concat(raw, audio, v=1, a=1).node
                stream = ffmpeg.output(joined[0], joined[1], 'scene%d.mp4' % (i+1)) 
                stream.run()

            shuffled = sorted(scene_list, key=lambda k: random.random())

            stream = 0
            video_list = []
            audio_list = []
            merge_list = []
            raw = ffmpeg.input(file)

            for i, scene in enumerate(shuffled):
                start = scene[0].get_timecode()
                end = scene[1].get_timecode()

                audio = (
                    raw
                    .filter_('atrim', start=start, end=end)
                    .filter_('asetpts', 'PTS-STARTPTS')
                )

                video = ffmpeg.trim(raw, start=start, end=end)
                video = video.setpts('PTS-STARTPTS')

                video_list.append(video)
                audio_list.append(audio)

                if (i == len(shuffled) - 1):
                    for i in range(len(video_list)):
                        merge_list.append(video_list[i])
                        merge_list.append(audio_list[i])

                    stream = ffmpeg.concat(*merge_list, v=1, a=1)
                    stream = ffmpeg.output(stream, 'new.mp4')
                    stream.run()

if __name__ == "__main__":
    main()