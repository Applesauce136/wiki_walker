from flask import *
import urllib2
import json

app = Flask(__name__)

@app.route("/tree/<node>")
def tree(node=""):
    pass

@app.route("/page/<title>")
def page(title="Main_Page"):
    page = ""
    add(title)
    urlfile = urllib2.urlopen("http://en.wikipedia.org/w/api.php?action=query&format=json&titles=%s&prop=links" % title)
    stuff = json.loads(urlfile.read())
    for outer in stuff["query"]["pages"]:
        page += "Links from %s:<br>\n" % stuff["query"]["pages"][outer]["title"]
        for inner in stuff["query"]["pages"][outer]["links"]:
            page += "<a href=%s>%s</a><br>\n" % (url_for("page", title=inner["title"]), inner["title"])
    return page

if __name__ == "__main__":
    app.run(debug=True)
