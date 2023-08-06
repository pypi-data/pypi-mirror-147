from html.parser import HTMLParser
from urllib.parse import urlparse

TAGS = ["link", "img", "video", "script", "a"]
ATTRS = ["href", "src"]

class Parser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag in TAGS:
            url = list(filter(lambda l: l[0] in ATTRS, attrs))

            if len(url) == 1:
                self._urls.add(url[0][1].strip())

    def __init__(self):
        super().__init__()
        self._urls = set()

def handle_relative_link(u, domain="", proto="http"):

        parsed = urlparse(u)

        if parsed._replace(netloc="").geturl() == u:

            if not u.startswith("/"):
                u = "/" + u

            u = domain + u

        parsed = urlparse(u)

        if parsed._replace(scheme="").geturl() == u:
            u = proto + "://" + u

        return u

def extract_links(text, domain="", proto="http"):
    parser = Parser()
    parser.feed(text)

    result = parser._urls

    result = { r for r in result if not r.startswith(("mailto", "e-name")) }

    result = { handle_relative_link(u, domain=domain, proto=proto) for u in result }

    return result
