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
        session['hist'] = {} #init session history
    if request.args.get("submit") == "submit":
        return redirect(url_for("page", title=request.args.get("search")))
    return render_template("home.html")

@app.route("/tree")
def tree():
    s = str(session['hist']) + "<hr>"
    for thing in session['hist']:
        s+= thing + "<br>"
        for item in session['hist'][thing][0]:
            s+= "	from: " + item + "<br>"
        for item in session['hist'][thing][1]:
            s+= "	to: " + item + "<br>"
        s += "<br>"
    return s

@app.route("/wiki/")
@app.route("/wiki/<title>")
def page(title="Main_Page"):
    title = title.replace(" ", "_")
    if 'prev' in session:
        my_utils.add(session['hist'], session['prev'], title)
    session['prev'] = title
    page = '<a href="%s"><input type=submit value="Go Home"></a><br>' % url_for("home")

    text = my_utils.api_req(other={
        "format":"json",
        "prop":"text",
        "action":"parse",
        "page":title
    })
    url = my_utils.api_req(other = {
        "format":"json",
        "titles":title,
        "prop":"links", 
        "pllimit":"max",
        "redirects":"",
    })

    #"http://en.wikipedia.org/w/api.php?action=query&format=json&titles=%s&prop=links&pllimit=max&redirects" % title
    urlfile = urllib2.urlopen(url)
    textfile= urllib2.urlopen(text)

    stuff = json.loads(urlfile.read())
    textstuff= json.loads(textfile.read())

    '''
    for outer in stuff["query"]["pages"]:
        page += "Links from %s:<br>\n" % stuff["query"]["pages"][outer]["title"]
        for inner in stuff["query"]["pages"][outer]["links"]:
            page += "<a href=%s>%s</a><br>\n" % (url_for("page", title=inner["title"].replace(" ", "_")), inner["title"])
    '''
    page+= "<hr>"
    page+= text + "<hr>"
    page += textstuff["parse"]["text"]["*"]
    return page

if __name__ == "__main__":
    app.run(debug=True)
