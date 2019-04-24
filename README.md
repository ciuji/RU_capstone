# RU_capstone

Rutgers ECE capstone(2019): Multilingual ASR data collection

## Introduction

Crawl multilingual audio and text reasources from web, achieve forced alignment on those data.

There would be two part of our project, the first is Crawler, the second is Aligner.

## Crawler

In this part, we achieved web crawling on two website. We crawled multilanguage audio and corresponding text data.

### WordProject

[WordProject](https://www.wordproject.org/) is a website that provide multilingual version of Bible. Actually, it support 37 languages. The reasources from this website have a perfect match rate.

### SBS News

[SBS News](https://www.sbs.com.au/radio/) is a news website that provide news in over 60 kinds of languages.

## Aligner

In this part, we achieved forced alignment based on [Montreal-Forced-Aligner](https://github.com/MontrealCorpusTools/Montreal-Forced-Aligner) and [Kaldi](https://github.com/kaldi-asr/kaldi) using the data we crawled before.

Our output would be [TextGrid](https://en.wikipedia.org/wiki/TextGrid) format files.

TextGrid demo:

![TextGrid photo](https://github.com/ciuji/RU_capstone/tree/master/docs/textgrid_demo.png)

## Video Demo

[demo](https://drive.google.com/file/d/1l5eDLmhOD4Y8sx-T78ZwsGGsQ1l7m31J/view?usp=sharing)

## Team Member

Mo Shi, Chaoji Zuo, Ziqi Wang, Zekun Zhang, Duc Le
