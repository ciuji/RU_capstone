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
	main_page = 'https://www.wordproject.org/bibles/'
	path = os.path.split(os.path.realpath(__file__))[0]
	# build a dictionary with all supported languages being the keys
	language_list = {}
	with open(path+'/'+'language_list.txt','r') as file:
		for line in file:
			line = line.strip('\n')
			t = line.split('-')
			language_list[t[0]] = t[1]
	while True:
		try:
			l = input('Please select your language: ').lower()
			choice = language_list[l]
			break
		except KeyError:
			print('Sorry, the language you entered is currently not supported. Please try another one.')
	return main_page + choice


def find_all_resources(link):
	resources = []
	# in total there are 66 scriptures in Bible
	for i in range(1,67):
		current_link = link + '/' + str(i).zfill(2) + '/'
		r = requests.get(url=current_link + '1.htm')
		soup = BeautifulSoup(r.text, 'html.parser')
		# add the first chapter
		resources.append(current_link + '1.htm')
		# add all other chapters
		for i in soup.find('div', class_='textHeader').find_all('a', class_='chap'):
			resources.append(current_link + i['href'][:-2])
	return resources


def is_string(x):
	return type(x) is bs4.element.NavigableString


def scrapper(link, index):
	r = requests.get(url=link)
	soup = BeautifulSoup(r.text, 'html.parser')
	audio = soup.find('a', title='Right Click and select Save As to Download')['href']
	a = soup.find('div', class_='textOptions')
	if type(a) == type(None):
		return
	text = a.text.upper()
	# remove punctuations and numbers
	eliminate_set = string.punctuation + string.digits + hanzi.punctuation
	replace_set = ' ' * len(eliminate_set)
	trans_tab = str.maketrans(eliminate_set, replace_set)
	text = text.translate(trans_tab)
	# current path where the program runs
	path = os.path.split(os.path.realpath(__file__))[0]
	# if used for the first time, create a folder for all resources
	if not os.path.isdir(path + '/bible'):	
		os.makedirs(path + '/bible')
	path += '/bible'
	# create a folder for current language if the folder never exists
	language = link.split('/')[-3]
	if not os.path.isdir(path + '/' + language):
		os.makedirs(path + '/' + language)
	path = path + '/' + language
	# if used for the first time, create folders for audio/text separately
	if not os.path.isdir(path + '/audio'):	
		os.makedirs(path + '/audio')
	audio_dir = path + '/audio'
	if not os.path.isdir(path + '/text'):	
		os.makedirs(path + '/text')
	text_dir = path + '/text'
	try:
		# get audio
		wget.download(audio, out=audio_dir + '/' + f'{index}.mp3')
		# format transformation
		ori = AudioSegment.from_file(audio_dir + '/' + f'{index}.mp3', format='mp3')
		ori = ori.set_frame_rate(44100)
		ori.export(audio_dir + '/' + f'{index}.wav', format='wav')
		# delete the original audio
		os.remove(audio_dir + '/' + f'{index}.mp3')
		# get text
		with open(text_dir + '/' + f'{index}.lab', 'w', encoding='utf-8') as f:
			f.write(text)
	except:
		with open(text_dir + '/' + f'{index}_empty.lab', 'w', encoding='utf-8') as f:
			pass

		
if __name__ == '__main__':
	
	link = language_selection()
	resources = find_all_resources(link)
	index = 0
	for item in resources:
		index += 1
		scrapper(item, index)
	'''
	link = 'https://www.wordproject.org/bibles/cz/01/1.htm' # please paste the link of the resource here
	scrapper(link, 1)
	'''
	