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

import media_aggregator
from json import loads as _l
import query_extractor as _qe
from flask_restful import Resource, reqparse
from media_aggregator import (shorten_news, get_gkg, GuardianAggregator as _ga, NYTAggregator as _nyt)


class QueryService(Resource):
    def post(self):
        args = parser.parse_args()
        result = clf.predict(args["data"])
        return result[0], 200 if result[1] else 400


class QueryAnalyzer(object):
    def __init__(self):
        self._query_extractor = _qe.QueryExtractor()

    def predict(self, data):
        try:
            if "news" in data.lower() or "latest" in data.lower():
                # News query
                source, query = self._query_extractor.get_news_tokens(data)
                response = (_ga() if "guardian" in source else _nyt()).get_news(query)
                if len(response) <= 0:
                    return {"phrase": "Sorry, no relevant results were returned."}, 500
                i, done = 0, media_aggregator.shorten_news(response[0])
                while (not done) and ((i + 1) < len(response)):
                    i += 1
                    done = shorten_news(response[i])
            else:
                # Knowledge query
                done = get_gkg(self._query_extractor.get_knowledge_tokens(data))
            ret_val = {"urls": done}
            if not done:
                ret_val["phrase"] = "Sorry, no valid results were returned."
            return ret_val, done
        except Exception, e:
            return {"phrase": "Sorry, something unexpected happened.", "original_exception": e.message}, False


parser = reqparse.RequestParser()
parser.add_argument("data")
clf = QueryAnalyzer()
