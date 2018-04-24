from pytube import YouTube
import pytube.extract
from pytube.helpers import safe_filename

import urllib.request
import urllib.error

from progress.bar import Bar

from utils import MissingArgument

import os
import argparse


def get_video(args, suffix=""):

    # get args
    url = args["url"]
    dest = os.path.dirname(args["output"])
    name = os.path.basename(args["output"])

    # check args
    if not url:
        raise MissingArgument("video: missing url")
    if not (dest or name):
        raise MissingArgument("video: missing output path")

    # download audio
    video = args["video"] = _download_video(url, dest, name + suffix)

    # return final path
    return video


def get_audio(args, suffix=""):

    # get args
    url = args["url"]
    dest = os.path.dirname(args["output"])
    name = os.path.basename(args["output"])

    # check args
    if not url:
        raise MissingArgument("audio: missing url")
    if not (dest or name):
        raise MissingArgument("audio: missing output path")

    # download audio
    audio = args["audio"] = _download_audio(url, dest, name + suffix)

    # return final path
    return audio

def get_image(args, suffix=""):

    # get args
    url = args["url"]
    dest = os.path.dirname(args["output"])
    name = os.path.basename(args["output"])

    # check args
    if not url:
        raise MissingArgument("image: missing url")
    if not (dest or name):
        raise MissingArgument("image: missing output path")

    # download image
    image = args["image"] = _download_image(url, dest, name + suffix + ".png")

    # return final path
    return image


def _download_video(url, dest, name):
    yt = YouTube(url, on_progress_callback=progress_bar, on_complete_callback=complete_bar)
    try:
        yt.streams\
            .filter(adaptive=True, mime_type="video/mp4")\
            .order_by('resolution')\
            .desc()\
            .first()\
            .download(output_path=dest, filename=name)
    except AttributeError:
        yt.streams \
            .filter(mime_type="video/mp4") \
            .order_by('resolution') \
            .desc() \
            .first() \
            .download(output_path=dest, filename=name)

    path = os.path.join(dest, name) + ".mp4"
    os.rename(os.path.join(dest, safe_filename(name)) + ".mp4", path)

    return path


def _download_audio(url, dest, name):
    yt = YouTube(url, on_progress_callback=progress_bar, on_complete_callback=complete_bar)

    try:
        yt.streams\
            .filter(mime_type="audio/mp4")\
            .order_by('abr')\
            .desc()\
            .first()\
            .download(output_path=dest, filename=name)
    except AttributeError:
        yt.streams \
            .filter(mime_type="video/mp4") \
            .first() \
            .download(output_path=dest, filename=name)

    path = os.path.join(dest, name) + ".mp4"
    os.rename(os.path.join(dest, safe_filename(name)) + ".mp4", path)

    return path


def _download_image(url, dest, name):
    image_url = "https://img.youtube.com/vi/" + pytube.extract.video_id(url) + "/maxresdefault.jpg"
    backup_url = "https://img.youtube.com/vi/" + pytube.extract.video_id(url) + "/0.jpg"

    path = os.path.join(dest, name)

    try:
        return urllib.request.urlretrieve(image_url, path)[0]
    except urllib.error.HTTPError:
        pass

    try:
        return urllib.request.urlretrieve(backup_url, path)[0]
    except urllib.error.HTTPError:
        pass

    return None

def yt_url(url):
    try:
        YouTube(url)
    except:
        raise argparse.ArgumentTypeError(url + " is not a valid youtube url")
    return url


# downloading progress
bar = None

def progress_bar(stream, chunk, file, bytes_remaining):
    global bar
    M = 1000000
    if not bar:
        bar = Bar(" Download", max=stream.filesize/M, suffix='%(index).3f/%(max).3f MB')

    bar.goto((stream.filesize - bytes_remaining)/M)

def complete_bar(stream, file):
    global bar
    bar = None
    print("")
