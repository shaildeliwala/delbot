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

from resources.query_service import QueryService
from flask_restful import Api, Resource, reqparse
from flask import Flask, render_template, send_from_directory


app = Flask(__name__)
api = Api(app)
api.add_resource(QueryService, '/news_urls')


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/favicon.ico")
def favicon():
    from os import path
    return send_from_directory(path.join(app.root_path, "static"), "favicon.ico", mimetype = "image/vnd.microsoft.icon")


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


if __name__ == '__main__':
    try:
        app.run('localhost', port = 5000, debug = True, use_reloader = False)
    except Exception, e:
        print e
