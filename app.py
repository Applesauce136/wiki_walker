from flask import *
import urllib2
import json
import wiki

app = Flask(__name__)

@app.route("/")
def home(methods = ["GET"]):
    if request.args.get("submit") == "Submit":
        return redirect(url_for("page", title=request.args.get("search")))
    return render_template("home.html")

@app.route("/tree/<node>")
def tree(node=""):
    pass

@app.route("/page/<title>")
def page(title="Main_Page"):
    page = "<a href='/'><input type=submit></a><br>"
    url = "http://en.wikipedia.org/w/api.php?action=query&format=json&titles=%s&prop=links&pllimit=max" %title
    urlfile = urllib2.urlopen(url)
    stuff = json.loads(urlfile.read())
    for outer in stuff["query"]["pages"]:
        page += "Links from %s:<br>\n" % stuff["query"]["pages"][outer]["title"]
        for inner in stuff["query"]["pages"][outer]["links"]:
            page += "<a href=%s>%s</a><br>\n" % (url_for("page", title=inner["title"]), inner["title"])
    return page

if __name__ == "__main__":
    app.run(debug=True)
