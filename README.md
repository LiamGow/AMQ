# AMQ

Requirements:
- python3
- ffmpeg:
    - https://github.com/adaptlearning/adapt_authoring/wiki/Installing-FFmpeg
    
usage: amq.py [-h] [-o OUTPUT] [-v VIDEO] [-a AUDIO] [-i IMAGE] [-u URL]
              [-r RESOLUTION] [-p FPS] [-b BITRATE] [-m] [-s] [-n] [-ss START]
              [-ee END]

A utility for downloading and converting youtube videos

# Optional Arguments:
    -h, --help                              Help: show this help message and exit
    
    -o OUTPUT, --output OUTPUT              Output: path - file extension is optional and discouraged
    
    -u URL, --url URL                       Input: youtube url to download video and/or audio from
    -v VIDEO, --video VIDEO                 Input: video - with or without audio
    -a AUDIO, --audio AUDIO                 Input: audio
    -i IMAGE, --image IMAGE                 Input: image for mp3 thumbnails and still videos
    
    -r RESOLUTION, --resolution RESOLUTION  Variable: vertical output resolution
    -p FPS, --fps FPS                       Variable: output frames per second
    -b BITRATE, --bitrate BITRATE           Variable: video bitrate in #K or #M
    -ss START, --start START                Variable: timestamp from the original to start the output at
    -ee END, --end END                      Variable: timestamp from the original to end the output at
    
    -m, --music                             Option: creates an mp3
    -s, --still                             Option: creates a video with a single still image (video thumbnail or provided)
    -n, --no_convert                        Option: do not convert downloaded files - this will not merge the audio and video tracks


# Input Precedence: 
(Lower numbers overwrite higher numbers of the same format)
1. Image
2. Audio
3. Video
4. URL
