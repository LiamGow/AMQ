# AMQ

Requirements:
- python3
- ffmpeg:
    - https://github.com/adaptlearning/adapt_authoring/wiki/Installing-FFmpeg
    
usage: amq.py [-h] [-o OUTPUT] [-v VIDEO] [-a AUDIO] [-i IMAGE] [-u URL]
              [-r RESOLUTION] [-p FPS] [-b BITRATE] [-m] [-s] [-n] [-ss START]
              [-ee END]

A utility for downloading and converting youtube videos

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        output path - file extension is optional and
                        discouraged
  -v VIDEO, --video VIDEO
                        video input - with or without audio
  -a AUDIO, --audio AUDIO
                        audio input
  -i IMAGE, --image IMAGE
                        image input for mp3 thumbnails and still videos
  -u URL, --url URL     youtube url to download video and/or audio from
  -r RESOLUTION, --resolution RESOLUTION
                        vertical output resolution
  -p FPS, --fps FPS     output frames per second
  -b BITRATE, --bitrate BITRATE
                        video bitrate in #K or #M
  -m, --music           creates an mp3
  -s, --still           creates a video with a single still image (video
                        thumbnail or provided
  -n, --no_convert      do not convert downloaded files - this will not merge
                        the audio and video tracks
  -ss START, --start START
                        timestamp from the original to start the output at
  -ee END, --end END    timestamp from the original to end the output at
