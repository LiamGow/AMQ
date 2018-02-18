import install
import download
import ffmpeg

from utils import MissingArgument

import sys
import argparse
from pathType import PathType


def get_args():
    parser = argparse.ArgumentParser(description="A utility for downloading and converting youtube videos")

    parser.add_argument('-o', "--output", action="store", type=PathType(exists=None, type="file"), help="output path - file extension is optional and discouraged")

    parser.add_argument('-v', "--video", action="store", type=PathType(exists=True, type="file"), help="video input - with or without audio")
    parser.add_argument('-a', "--audio", action="store", type=PathType(exists=True, type="file"), help="audio input")
    parser.add_argument('-i', "--image", action="store", type=PathType(exists=True, type="file"), help="image input for mp3 thumbnails and still videos")
    parser.add_argument('-u', "--url", action="store", type=download.yt_url, help="youtube url to download video and/or audio from")

    parser.add_argument('-r', "--resolution", action="store", type=int, help="vertical output resolution")
    parser.add_argument('-p', "--fps", action="store", type=int, help="output frames per second")
    parser.add_argument('-b', "--bitrate", action="store", default="500K", type=ffmpeg.bitrate, help="video bitrate in #K or #M")

    parser.add_argument('-m', "--music", action="store_true", help="creates an mp3")
    parser.add_argument('-s', "--still", action="store_true", help="creates a video with a single still image (video thumbnail or provided")
    parser.add_argument('-n', "--no_convert", action="store_true", help="do not convert downloaded files - this will not merge the audio and video tracks")

    parser.add_argument('-ss', "--start", action="store", type=ffmpeg.timecode, help="timestamp from the original to start the output at")
    parser.add_argument('-ee', "--end", action="store", type=ffmpeg.timecode, help="timestamp from the original to end the output at")

    return vars(parser.parse_args(sys.argv[1:]))

def main():

    # parse and get args as dict
    args = get_args()

    # debug print args
    # print(args)

    # catch and print any argument errors
    try:
        ffmpeg.process(args)
    except MissingArgument as e:
        print(e)

if __name__ == "__main__":
    main()
