#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  1 10:49:44 2019

@author: ciuji
"""
import re 
import urllib.request
import requests
import bs4
import time
import json
root_url = 'http://pyvideo.org'
index_url ='https://news.rthk.hk/rthk/ch/video-gallery.htm'
#ffmpeg -i hello.mp4 -f wav -ar 44100  test.wav
#%% basic newscralwer
class newsCrawler:
    def __init__(self,link):
        self.url=link
        self.mp4_name=""
        self.mp4_url=""
        self.vid=""
        


    def get_video_url(self):
        response = requests.get(self.url)
        soup = bs4.BeautifulSoup(response.text,features='lxml')
        #print(response.text)
        #print(soup.get_text())
    
        new_title=soup.find(property="og:title")['content']
        self.mp4_name=new_title + ".mp4"
        print(soup.find(property="og:description")['content'])
        print(soup.find(property="og:video:url")['content'])
        self.mp4_url=soup.find(property="og:video:url")['content']
        #eturn soup.find_all('meta')
        return self.mp4_url

    def download_mp4(self):
        start = time.time()
        urllib.request.urlretrieve(self.mp4_url, self.mp4_name)
        end = time.time()
        print ('Finish in ：', end - start)


# =============================================================================
# nc=newsCrawler(index_url)
# print(nc.get_video_url())
# #nc.download_mp4()
# =============================================================================


#%% list of video and introtext
from selenium import webdriver

'''
driver = webdriver.PhantomJS(executable_path="/Users/ciuji/Applications/phantomjs-2.1.1/bin/phantomjs")
driver.get(index_url)
time.sleep(4)
introTextElementList=driver.find_elements_by_class_name("videoNewsIntroText")
introTextList=[]
for ii in introTextElementList:
    introTextList.append(ii.get_attribute("data-introtext"))
    
videoLinkElementList=driver.find_elements_by_class_name("videoNewsVideoPath")
videoLinkList=[]
for ii in videoLinkElementList:
    videoLinkList.append(ii.get_attribute("innerHTML"))
    print (ii.get_attribute("innerHTML"))
 '''

class newsListCrawler:
    def __init__(self,link):
        self.url=link
        self.introTextList=[]
        self.videoList=[]
        
    def getList(self):
        driver = webdriver.PhantomJS(executable_path="/Users/ciuji/Applications/phantomjs-2.1.1/bin/phantomjs")
        driver.get(self.url)
        time.sleep(4)
        introTextElementList=driver.find_elements_by_class_name("videoNewsIntroText")
        for ii in introTextElementList:
            self.introTextList.append(ii.get_attribute("data-introtext"))
            
        videoLinkElementList=driver.find_elements_by_class_name("videoNewsVideoPath")
        for ii in videoLinkElementList:
            self.videoList.append(ii.get_attribute("innerHTML"))
            print (ii.get_attribute("innerHTML"))
        
    def download_videos(self):
        if (self.videoList==[]):
            print("empty list")
            return
        partVideoUrl="https://newsstatic.rthk.hk/videos/"
        for ii,singleID in enumerate(self.videoList):
            singleUrl=partVideoUrl+singleID
            start = time.time()
            urllib.request.urlretrieve(singleUrl, "crawler_download/"+singleID)
            json.dump(self.introTextList[ii],open("crawler_download/"+singleID+".json",'w'))
            end = time.time()
            print ('{name} finish in:{time}'.format(name=singleID,time= end - start))
nc=newsListCrawler(index_url)
nc.getList()
#nc.download_videos()    

# todo 去掉 </br>