def api_req(action="query", other={}):
    out = "http://en.wikipedia.org/w/api.php?action=%s" % (action)
    for word in other:
        out += "&%s=%s" % (word, other[word])
    return out
