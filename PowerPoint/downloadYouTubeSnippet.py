# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 08:20:38 2023

@author: alexander.busch@alumni.ntnu.no
"""

from pytube import YouTube
from moviepy.video.io.VideoFileClip import VideoFileClip
import os

# Ask user to input the YouTube video URL and time range
url = r'https://www.youtube.com/watch?v=z4HCwWKC8Iw'
start_time = 0.1
end_time = 23
path = r'C:\aaa'

 # Create a YouTube object and get the video
youtube = YouTube(url)
video = youtube.streams.get_highest_resolution()
if not os.path.exists(path):
    os.makedirs(path)

# Download the video and save it to a file
video_path = video.download(path)

# Use moviepy to extract the specified time range of the video
video_clip = VideoFileClip(video_path)
extracted_clip = video_clip.subclip(float(start_time), float(end_time))
extracted_clip_filename = f"{video_path.removesuffix('.mp4')} - start {start_time}s - end {end_time}s.mp4"

extracted_clip.write_videofile(extracted_clip_filename)

# Alternatively, wrap in function
#def downloadYT(url,path, start_time,end_time):
#video_path = downloadYT(url, path, start_time,end_time)