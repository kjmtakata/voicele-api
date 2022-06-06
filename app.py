import hashlib
import os
import re
import string

import bs4
import flask
import flask_restful
import requests

app = flask.Flask(__name__)
api = flask_restful.Api(app)
BASE_URL = "https://quizmasters.biz/DB/Audio/Voices"


class Answer(flask_restful.Resource):
    def get(self, date):
        links = get_links()
        index = int.from_bytes(hashlib.sha256(date.encode()).digest(), "big") % len(
            links
        )
        link = links[index]
        return {
            "name": get_name(link),
            "url": get_url(link),
        }


class OptionList(flask_restful.Resource):
    def get(self):
        return [get_name(link) for link in get_links()]


def get_links():
    page = requests.get(f"{BASE_URL}/Guess%20The%20Voice.html")
    soup = bs4.BeautifulSoup(page.content, "html.parser")
    return soup.find_all("a", {"href": re.compile("^[^#]")})


def get_name(link):
    return link.getText().rstrip(string.digits).strip()


def get_url(link):
    return f'{BASE_URL}/{link["href"]}'


api.add_resource(Answer, "/answers/<string:date>")
api.add_resource(OptionList, "/options")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
