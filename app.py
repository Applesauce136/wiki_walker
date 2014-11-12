from flask import *
import urllib2
import json
import my_utils

app = Flask(__name__)
app.secret_key = "asdf"

@app.route("/")
def home(methods = ["GET"]):
    if not 'hist' in session:
        session['hist'] = {}
    if request.args.get("submit") == "submit":
        my_utils.add(hist, "Searched for", request.args.get("search"))
        return redirect(url_for("wiki", title=request.args.get("search")))
    return render_template("home.html")

@app.route("/tree")
def tree():
    if 'prev' in session:
        session.pop('prev')
    return render_template("tree.html", thing=session['hist'])

@app.route("/wiki/")
@app.route("/wiki/<title>")
def wiki(title="Main_Page"):
    title = title.replace(" ", "_")
    if not 'hist' in session:
        session['hist'] = {}
    if 'prev' in session:
        my_utils.add(session['hist'], session['prev'], title)
    session['prev'] = title

    text = my_utils.api_req(other={
        "action":"parse",
        "format":"json",
        "page":title,
        "prop":"text",
        "redirects":"",
    })
    url = my_utils.api_req(other = {
        "action":"query",
        "format":"json",
        "titles":title,
        "prop":"links", 
        "pllimit":"max",
        "redirects":"",
    })

    try:
        urlfile = urllib2.urlopen(url)
    except UnicodeEncodeError:
        return "Placeholder error message<hr>Our website doesn't like URL's with UTF-8 only characters (aka IRI's) yet.  If possible, maybe you could manually edit the URL you're requesting to be ASCII-compliant?"

    textfile= urllib2.urlopen(text)

    stuff = json.loads(urlfile.read())
    textstuff= json.loads(textfile.read())

    '''
    for outer in stuff["query"]["pages"]:
        page += "Links from %s:<br>\n" % stuff["query"]["pages"][outer]["title"]
        for inner in stuff["query"]["pages"][outer]["links"]:
            page += "<a href=%s>%s</a><br>\n" % (url_for("page", title=inner["title"].replace(" ", "_")), inner["title"])
    '''
    page = textstuff["parse"]["text"]["*"]
    return render_template("wiki.html", title=title, page=page)

@app.route("/clear", methods=["GET"])
def clear():
    if request.args.get("submit") == "Yes":
        session['hist'] = {}
        return redirect(url_for("home"))
    return render_template("clear.html")
    
if __name__ == "__main__":
    app.run(debug=True)
