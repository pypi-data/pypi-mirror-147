# voltfpipe

A pipeline manager for a voltf project (photogrammetry and videogrammetry).

# Description
Initially, can manage raw videos (breaking them up)

# Requirements

`ffmpeg` available on the command line

# Quickstart

## Install
pip install voltfpipe

## How do I ... ?

### Init a project

`voltfpipe init`

### Add a video

`voltfpipe video add path/to/video --project my-project --video my-video-slug` 

### Add all  videos in a directory

`voltfpipe videos add path/to/videos/ --project my-project` 

### Prepare a video for import 

`voltfpipe video configure --project my-project --video my-video-slug`

### Batch Prepare all videos for import 

`voltfpipe videos configure --project my-project`

This will guestimate a lot of settings for each video.

### Create images for a project

`voltfpip images create --project my-project`

Images will be in `my-project/images/`

