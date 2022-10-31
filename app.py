from flask import Flask, render_template, request
from flask_session import Session
import pyshorteners

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template('index.html')
    else:
        type = request.form.get("type")
        lurl = request.form.get("longUrl")
        print(type)
        print(lurl)

        if not type or not lurl:
            return render_template('error.html') 
        elif type == "bitly":
            shortener = pyshorteners.Shortener(api_key='2397da4b4ef52c663606be8d89d95b9992996919')
            surl = shortener.bitly.short(lurl)
        elif type == "tinyurl":
            shortener = pyshorteners.Shortener()
            surl = shortener.tinyurl.short(lurl) 
        else:
            return render_template('error.html')
        
        return render_template('url.html', surl=surl)