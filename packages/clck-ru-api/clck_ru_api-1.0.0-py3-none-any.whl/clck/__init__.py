import requests as r
class ru:
    def link(url):
        return r.get("http://clck.ru/--?url=%s" % url).text


