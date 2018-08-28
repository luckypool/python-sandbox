# -*- coding: utf-8 -*-

import re
import urllib.request
from bs4 import BeautifulSoup

class NovelBase:
    base_url = "https://ncode.syosetu.com"

class Paragraph:
    def __init__(self, paragraph_no, text):
        self._paragraph_no = paragraph_no
        self._text         = text
        self._is_speech    = self.__is_speech()
        self._is_blank     = self.__is_blank()

    @classmethod
    def from_bs(cls, bs_object):
        # ex.)   <p id="L1">「あんなものがあるものか！」</p>
        paragraph_no = int(bs_object["id"].replace("L", ""))
        # 全角スペース削除
        text = bs_object.text.replace("\u3000","")
        return cls(paragraph_no, text)

    @property
    def paragraph_no(self):
        return self._paragraph_no

    @property
    def text(self):
        return self._text

    @property
    def is_blank(self):
        return self._is_blank

    @property
    def is_speech(self):
        return self._is_speech

    def __is_speech(self):
        speech_regexp = r'^「.+?」$'
        match = re.match(speech_regexp, self.text)
        return False if match is None else True

    def __is_blank(self):
        blank_regexp = r'^$'
        match = re.match(blank_regexp, self.text)
        return False if match is None else True

class EpisodeContent:
    def __init__(self, url):
        self._url   = url
        self._paragraph = None

    def __init_content(self):
        html = urllib.request.urlopen(self._url)
        bs   = BeautifulSoup(html, "lxml")
        paragraph = bs.select("div#novel_honbun p")
        self._bs = bs
        self._paragraph = list(map(lambda l: Paragraph.from_bs(l), paragraph))

    @property
    def paragraph(self):
        if self._paragraph is None:
            self.__init_content()
        return self._paragraph

class Episode(NovelBase):
    def __init__(self, title, url):
        self.title = title
        self.url   = url
        self._content = EpisodeContent(url)

    @classmethod
    def from_bs(cls, bs_object):
        a_tag = bs_object.find("a")
        title = a_tag.text
        url   = cls.base_url + a_tag["href"]
        return cls(title, url)

    @property
    def content(self):
        return self._content

class Novel(NovelBase):
    def __init__(self, product_id):
        self._product_id = product_id
        self.__init_bs4()

    def __init_bs4(self):
        url  = self.base_url + '/' + self._product_id
        html = urllib.request.urlopen(url)
        bs   = BeautifulSoup(html, "lxml")
        episodes = bs.select("div#novel_contents div.index_box .novel_sublist2")
        self._bs       = bs
        self._author   = bs.select("div#novel_contents div.novel_writername a")[0]
        self._episodes = list(map(lambda e: Episode.from_bs(e), episodes))

    @property
    def product_id(self):
        return self._product_id

    @property
    def author(self):
        return self._author

    @property
    def episodes(self):
        return self._episodes

