"""
Delbot

Copyright (C) 2017  Shail Deliwala

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import requests as _req
import wikipedia as _wk
from re import findall as _findall


_guardian_key = ""
_nyt_key = ""
_guardian_url = "http://content.guardianapis.com/search"
_nyt_url = "https://api.nytimes.com/svc/search/v2/articlesearch.json"


class MediaAggregatorMixin:
    """
    This is the base class for all current and future media aggregators.
    """
    def __init__(self):
        pass

    def get_news(self, query):
        pass

    def get_limit(self):
        pass


class GuardianAggregator:
    def __init__(self):
        self._params = {"q": "", "api-key": _guardian_key}
        self._limit = None

    def get_news(self, query):
        self._params["q"] = str(query)
        response = _req.get(_guardian_url, params = self._params)
        # self._limit = response.headers["X-RateLimit-Remaining-day"]
        return [x["webUrl"] for x in response.json()["response"]["results"] if x["type"] == "article" and
                x["sectionName"] != u"Media" and "quiz" not in x["webUrl"].lower()]

    def get_limit(self):
        if not self._limit:
            self.get_news("test")
        return self._limit


class NYTAggregator:
    def __init__(self):
        self._params = {"q": "", "api-key": _nyt_key}

    def get_news(self, query):
        self._params["q"] = str(query)
        response = _req.get(_nyt_url, params = self._params)
        return [x["web_url"] for x in response.json()["response"]["docs"] if x["type_of_material"] == "News"]

    def get_limit(self):
        return self._limit


def shorten_news(url, n = 5):
    from bs4 import BeautifulSoup as bs
    from summarizer import FrequencySummarizer as fs
    response = _req.get(url)
    if not response.ok:
        return False
    page = response.content
    soup = bs(page, "lxml")
    summary = fs().summarize("\n".join([x.text for x in soup.findAll("p") if len(x.text.split()) > 1]), n)
    summary.insert(0, soup.title.text)
    return ' '.join(summary)


def get_gkg(query):
    try:
        s = _wk.summary(query, sentences = 5)
        for x in _findall("\(.*\)", s):
            s = s.replace(x, "")
        return s
    except _wk.DisambiguationError, e:
        return False
