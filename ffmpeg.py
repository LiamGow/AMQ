import argparse
import subprocess

import download
from utils import MissingArgument

import os
import sys

# ffmpeg location
ffmpeg_path = "ffmpeg" if sys.platform.startswith('win') else "./ffmpeg"

def process(args):

    # get args
    dest = args["output"]

    video = args["video"]
    audio = args["audio"]
    image = args["image"]
    url = args["url"]

    resolution = args["resolution"]
    bitrate = args["bitrate"]
    fps = args["fps"]

    music = args["music"]
    still = args["still"]
    no_convert = args["no_convert"]

    start = args["start"]
    end = args["end"]

    # create ffmpeg args with libraries
    start_time_flag = ""
    end_time_flag = ""
    input_flags = ""
    output_flags = ""

    # trimming
    if start:
        start_time_flag += " -ss " + start
    if end:
        end_time_flag += " -to " + end

    # audio codec
    if music:
        input_flags += " -c:a copy"
    else:
        input_flags += " -c:v libvpx-vp9 -c:a libvorbis"

    # create output args
    if dest and not os.path.splitext(dest)[1]:
        dest += ".webm" if not music else ".mp3"

    # check args

    # check for dest, or something to use as dest
    video_split = os.path.splitext(video) if video else False
    audio_split = os.path.splitext(audio) if audio else False
    dest_video = dest == video_split[0] if video else False
    dest_audio = dest == audio_split[0] if audio else False

    if (not dest) or dest_video or dest_audio:
        # use name of audio or video if available, appending " out" if the same extension
        if video:
            dest = video
            if not resolution:
                video = video_split[0] + "_old" + video_split[1]
                try: os.remove(video)
                except: pass
                os.rename(dest, video)

        elif audio:
            dest = audio
            if not resolution:
                audio = audio_split[0] + "_old" + audio_split[1]
                try: os.remove(audio)
                except: pass
                os.rename(dest, audio)

        else:
            raise MissingArgument("no output filepath given")

    # handle audio track only
    if music or still:

        # if audio not provided
        if not audio:
            # get audio from url
            if url:
                audio = download.get_audio(args)
            # or error if no url
            else:
                raise MissingArgument("no audio file or url given for music/still")

        # if image not provided
        if not image:
            # get image from url
            if url:
                image = download.get_image(args, "_image")
            # or error if no url
            elif still:
                raise MissingArgument("no image or url given for music/still")

        # if no convert desired, end here
        if no_convert:
            return audio

        # add flag for still
        if still:
            output_flags += " -shortest"

        # convert audio to mp3
        if os.path.splitext(audio)[1] != ".mp3":
            temp = audio_convert(audio)
            os.remove(audio)
            audio = temp

        if music and image:
            input_flags += ' -map 0 -map 1 -metadata:s:v title="Album cover"'

    # handle video
    else:
        # if video not provided
        if not video:
            # download from url
            if url:
                video = download.get_video(args, " video")

                # if audio is not included in video file, also download audio
                probe = "ffprobe -loglevel error -select_streams a -show_entries stream=codec_type -of csv=p=0 "
                rtn = subprocess.run(probe + '"' + video + '"', stdout=subprocess.PIPE).stdout
                if not audio and "audio" not in rtn.decode('ascii'):
                    audio = download.get_audio(args, " audio")

            else:
                raise MissingArgument("process: no video file or url given")

        # return video after download if no_convert
        if no_convert:
            return video

        # output transformations
        if resolution:
            output_flags += " -vf scale=-1:" + str(resolution)
            dest_split = os.path.splitext(dest)
            dest = dest_split[0] + " " + str(resolution) + "p" + dest_split[1]
        if bitrate:
            output_flags += " -b:v " + bitrate
        if fps:
            output_flags += " -r:v " + str(fps)

    # create ffmpeg command
    command = ffmpeg_path + " " + start_time_flag

    if image:
        if not music:
            command += ' -loop 1'
        command += ' -i "' + image + '"'
    if video and not image:
        command += ' -i "' + video + '"'
    if audio:
        command += ' -i "' + audio + '"'
    if input_flags:
        command += " " + input_flags

    command += " " + end_time_flag + " " + output_flags + ' "' + dest + '"'

    print(command)

    # run ffmppeg
    subprocess.run(command)

    # remove temp audio/video files
    if url and not no_convert:
        if video and os.path.isfile(video):
            os.remove(video)

        if audio and os.path.isfile(audio):
            os.remove(audio)

        if image and os.path.isfile(image):
            os.remove(image)

    # return final path
    return dest

def audio_convert(path):
    mp3 = os.path.splitext(path)[0] + "_temp.mp3"
    command = ffmpeg_path + ' -i "' + path + '" -q:a 0 -map a "' + mp3 + '"'
    print(command)
    subprocess.run(command)

    return mp3

def timecode(string):
    parts = string.split(":")
    try:
        for part in parts[:-1]:
            int(part)
        float(parts[-1])
    except ValueError:
        raise argparse.ArgumentTypeError(string + " is not a valid timecode")

    return string

def bitrate(string):
    try:
        int(string[:-2])
        if string[-1] not in ["K", "M"]:
            raise ValueError
    except ValueError:
        raise argparse.ArgumentTypeError(string + " is not a valid bitrate")

    return string
