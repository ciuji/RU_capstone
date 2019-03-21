# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 20:36:19 2019

@author: Duc Le
"""

import youtube_dl
import requests
import time

class audio_download:
    def __init__ (self, path = r'C:\Users\Duc Le\Desktop\SBSaudio\Audio', form = 'wav'):
        self.form = form   # '.wav', '.mp3' 
        self.path = path   # declare a path where to store the audio
        self.download_time = []  # measure the download time
        
    def download(self, url, name):
        # create a list of options before downloading
        ydl_opts = {
            'ignoreerrors': False,    # stop downloading during errors
            'quiet': True,            # show nothing to the stdout
            'no_warnings': True,      # no warnings shown to the stdout
            'format': 'bestaudio/best', # choose the best format it could download
            'postprocessors': [{  
            'key': 'FFmpegExtractAudio', 
            'preferredcodec': self.form,
            'preferredquality': '192',
            }],
            'noplaylist':True,
            'nocheckcertificate': True,
            'outtmpl': self.path + '\\' + name + '.%(etx)s',
        }

        # download the audio
        start_time = time.time()    # start time of downloading 
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            end_time = time.time()   # end time of downloading
            self.download_time.append(end_time - start_time)  # calculate the download time
  