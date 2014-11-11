from flask import *
import urllib2
import json
import my_utils

app = Flask(__name__)
app.secret_key = "asdf"

@app.route("/")
def home(methods = ["GET"]):
    if 'prev' in session:
        session.pop('prev')
    if not 'hist' in session:
        session['hist'] = {}
    if request.args.get("submit") == "Submit Query":
        return redirect(url_for("page", title=request.args.get("search")))
    return render_template("home.html")

@app.route("/tree/<node>")
def tree(node=""):
    return str(session['hist'])

@app.route("/page/<title>")
def page(title="Main_Page"):
    if 'prev' in session:
        my_utils.add(session['hist'], session['prev'], title)
    session['prev'] = title
    page = '<a href="%s"><input type=submit value="Go Home"></a><br>' % url_for("home")

    url = my_utils.api_req(other = {
        "format":"json",
        "titles":title,
        "prop":"links", 
        "pllimit":"max",
        "redirects":"",
    })
    #"http://en.wikipedia.org/w/api.php?action=query&format=json&titles=%s&prop=links&pllimit=max&redirects" % title
    urlfile = urllib2.urlopen(url)
    stuff = json.loads(urlfile.read())

    for outer in stuff["query"]["pages"]:
        page += "Links from %s:<br>\n" % stuff["query"]["pages"][outer]["title"]
        for inner in stuff["query"]["pages"][outer]["links"]:
            page += "<a href=%s>%s</a><br>\n" % (url_for("page", title=inner["title"].replace(" ", "_")), inner["title"])
    return page

if __name__ == "__main__":
    app.run(debug=True)
