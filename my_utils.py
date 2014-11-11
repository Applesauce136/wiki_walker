def api_req(action="query", other={}):
    out = "http://en.wikipedia.org/w/api.php?action=%s" % (action)
    for word in other:
        out += "&%s=%s" % (word, other[word])
    return out

def add(hist, prev, title):
    if not prev in hist:
        hist[prev] = ( [], [] )
        #init; read (camefrom, wentto)
    if not title in hist:
        hist[title] = ( [], [] )
    hist[title][0].append(prev)
    hist[prev][1].append(title)

