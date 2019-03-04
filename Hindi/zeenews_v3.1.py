# 3rd version of crawler for 'zeenews'
# update for crawler details

# import libraries
import requests
from fake_useragent import UserAgent
from selenium import webdriver
from lxml import etree
from time import sleep
import subprocess


# use the selenium web driver to get the source page
def web_driver():
    # selenium get request with headless options
    main_page_url = "https://zeenews.india.com/hindi/videos"
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get(main_page_url)
    # selenium scroll operation
    # in the zeenews page this scroll pixels can get 2500 urls
    js = 'document.documentElement.scrollTop = 1000000'
    driver.execute_script(js)
    sleep(10)
    # get the html of the main page which contains the urls of videos
    main_page_html = driver.page_source
    driver.quit()
    return main_page_html


# parse the html and get the video page urls
def get_urls(main_page_html):
    e = etree.HTML(main_page_html)
    video_page_urls = []
    base_url = "https://zeenews.india.com{}"
    post_urls = e.xpath('//div[@class = "mini-video mini-video-h margin-bt30px"]/a/@href')
    time_limits = e.xpath(
        '//div[@class = "mini-video mini-video-h margin-bt30px"]/a//span[@class="zeev-time zvd"]/text()')
    '''
    this filter is to judge whether videos' length are below 5 minutes or not
    when the pixels the webdriver scrolled is 1000000, we can get about 2500 urls in total,
    and after the filter only 1400 left
    '''
    for post_url, time_limit in zip(post_urls, time_limits):
        if int(str(time_limit)[0]) == 0 and int(str(time_limit)[1]) <= 4 and str(time_limit)[2] == ':':
            video_page_urls.append(base_url.format(post_url))
    return video_page_urls


# get the html of one video page
def get_html(video_page_url):
    # request and get html in response
    response = requests.get(video_page_url, headers={"User-Agent": UserAgent().random})
    # return raw html wait for parsing
    return response


# parse the html and return data in txt and video url
def parse_html(raw_html):
    e = etree.HTML(raw_html.text)
    video_url = e.xpath('string(//div/@video-code)')
    title = "".join(e.xpath('//div/h1/text()'))
    text = "".join(e.xpath('//div/p[@class="margin-bt10px"]/text()'))
    data = title + '\n' + text + '\n\n'
    print(video_url)
    print(data)
    return data, video_url


# first version for file writing
# def save_text(data):
#     with open('Zeenews_text.txt', 'a', encoding='utf-8') as f:
#         f.write(data)

# second version for file writing--less resources would be used in open file
def open_file():
    filename = open('Zeenews_text.txt', 'a', encoding='utf-8')
    return filename


def save_text(data, filename):
    filename.write(data)


def close_file(filename):
    filename.close()


# TODO (Zekun Zhang): Need to know the exact format for audio file and rewrite this part
# using ffmpeg in the terminal to download the video and transform the video
def video_extract(video_url, number):
    subprocess.check_call(
        ["ffmpeg", "-i", video_url, "hindi_" + str(number) + ".mp4"])


if __name__ == '__main__':
    main_page = web_driver()
    video_page = get_urls(main_page)
    # using a variable to do the counting work
    number = 0
    file = open_file()

    for url in video_page:
        number += 1
        html = get_html(url)
        data, video_url = parse_html(html)
        save_text(data, file)
        video_extract(video_url, number)

        # control the number of resource we need
        if number == 5:
            break

    close_file(file)
