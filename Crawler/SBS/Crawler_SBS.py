# -*- coding: utf-8 -*-

import requests
import bs4
from bs4 import BeautifulSoup
import os
import sys
import wget
from pydub import AudioSegment
import time
import string
from zhon import hanzi


def language_selection():
	main_page = 'https://www.sbs.com.au/radio/yourlanguage_podcasts'
	r = requests.get(url=main_page)
	soup = BeautifulSoup(r.text, 'html.parser')
	language_list = soup.find_all('div', class_="field field-name-field-list-url field-type-link-field field-label-hidden")
	links = {i.a.string.lower(): i.a['href'] for i in language_list}
	unsupported_list = ['assyrian','croatian','hebrew','lao','living black','punjabi','portuguese']
	while True:
		try:
			#l = 'mandarin'
			l = input('Please select your language: ').lower()
			if l in unsupported_list:
				raise KeyError
			choice = links[l]
			break
		except KeyError:
			print('Sorry, the language you entered is currently not supported. Please try another one.')
	if l == 'spanish' or l == 'tigrinya':
		return choice
	r = requests.get(url=choice)
	soup = BeautifulSoup(r.text, 'html.parser')
	for i in soup.find_all('a', class_="language-toggle"):
		if i.string != 'English':
			return 'https://www.sbs.com.au' + i['href']


def find_all_resources(link, max_pages=10):
	resources = []
	pages = max_pages
	current_link = link
	while pages != 0:
		pages -= 1
		r = requests.get(url=current_link)
		soup = BeautifulSoup(r.text, 'html.parser')
		# get all resource links on current page
		for i in soup.find_all('div', class_='audio__player-info'):
			resources.append(i.div.next_sibling.next_sibling.a['href'])
		if pages != 0:
			current_link = 'https://www.sbs.com.au' + soup.find('li', class_='pager-next').a['href']
	return resources


def is_string(x):
	return type(x) is bs4.element.NavigableString


def time_is_shorter_than(time, max_time):
	t1 = time.split()
	# if longer than 1 hour or less than 1 minute, exclude it
	if len(t1) != 4:
		return False
	t2 = max_time.split()
	if int(t1[0]) < int(t2[0]):
		return True
	elif int(t1[0]) == int(t2[0]):
		if int(t1[2]) <= int(t2[2]):
			return True
	return False


def text_is_longer_than(length, min_text):
	return length >= min_text


def filtering(time, length, max_time='8 min 0 sec', min_text=100):
	return time_is_shorter_than(time, max_time) and text_is_longer_than(length, min_text)


def scrapper(link):
	r = requests.get(url=link)
	soup = BeautifulSoup(r.text, 'html.parser')
	t = soup.find('div', class_='ds-1col')
	# if resource is not find, return directly
	if type(t) == type(None):
		return
	audio = t.find('source')['src']
	des = t.find('div', itemprop='description', recursive=False)
	text = des.p.string
	if type(text) == type(None):
		text = ''
	para = t.find('div', class_='field-type-text-with-summary', recursive=False)
	# determine if the news contains summary paragraphs
	if type(para) is not type(None):
		s = ''
		for i in para.div.div.find_all('p', recursive=False):
			# not an empty paragraph
			if len(i.contents) is not 0:
				# is the string that contains contents wanted
				if is_string(i.contents[0]):
					s += i.contents[0].string
		text += s
	# remove punctuations and numbers
	eliminate_set = string.punctuation + string.digits + hanzi.punctuation
	replace_set = ' ' * len(eliminate_set)
	trans_tab = str.maketrans(eliminate_set, replace_set)
	text = text.translate(trans_tab).upper()
	'''
	# filtering
	audio_length = str(t.find('div', class_='field-name-field-duration').contents[1])
	text_length = len(text)
	if not filtering(audio_length, text_length):
		return
	'''
	# current path where the program runs
	path = os.path.split(os.path.realpath(__file__))[0]
	# if used for the first time, create a folder for all resources
	if not os.path.isdir(path + '/resources'):	
		os.makedirs(path + '/resources')
	path += '/resources'
	# create a folder for current language if the folder never exists
	language = link.split('/')[-4]
	if not os.path.isdir(path + '/' + language):
		os.makedirs(path + '/' + language)
	path = path + '/' + language
	# use the name of the news to create audio/text files
	file_name = link.split('/')[-1]
	# return directly if the resource has already existed
	if os.path.isdir(path + '/' + file_name):
		return
	else:
		os.makedirs(path + '/' + file_name)
	path = path + '/' + file_name
	# get text
	
	with open(path + '/' + f'{file_name}.lab', 'w', encoding='utf-8') as f:
		f.write(text)
	# get audio
	wget.download(audio, out=path + '/' + f'{file_name}.mp3')
	# format transformation
	ori = AudioSegment.from_file(path + '/' + f'{file_name}.mp3', format='mp3')
	ori = ori.set_frame_rate(44100)
	ori.export(path + '/' + f'{file_name}.wav', format='wav')
	# delete the original audio
	os.remove(path + '/' + f'{file_name}.mp3')

		
if __name__ == '__main__':
	'''
	link = language_selection()
	t0 = time.time()
	resources = find_all_resources(link)
	for item in resources:
		scrapper('https://www.sbs.com.au' + item)
	print(time.time() - t0)
	''' 
	link = 'https://www.sbs.com.au/yourlanguage/bulgarian/bg/audiotrack/federalniyat-byudzhet-2019-na-avstraliya-e-veche-fakt' # please paste the link of the resource here
	scrapper(link)
	