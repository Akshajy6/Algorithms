from flask import Flask, flash, render_template, request, redirect
from flask_session import Session
from werkzeug.utils import secure_filename
import pyshorteners
import qrcode
import os

ALLOWED_EXTENSIONS = ['png' ,'jpg' ,'jpeg', 'webp', 'heic']

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_TYPE"] = "filesystem"
app.config["UPLOAD_FOLDER"] = r"static\uploads"
app.config["MAX_CONTENT_LENGTH"] = 32 * 1000 * 1000 * 1000
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
        service = request.form["service"]
        if service == "URL Shortener/QR Code Generator":
            return redirect("/urltools")
        elif service == "Image File Conversion":
            return redirect("/imagetools")
        else:
            return redirect("error.html")
        
@app.route("/urltools", methods=["GET", "POST"])
def urltools():
    if request.method == "GET":
        return render_template("urlinput.html")
    else:
        type = request.form.get("type")
        lurl = request.form.get("longUrl")
        
        if not type or not lurl:
            return render_template("error.html") 
        elif type == "bitly":
            print(os.getenv("API_KEY"))
            shortener = pyshorteners.Shortener(api_key="2397da4b4ef52c663606be8d89d95b9992996919") #Bitly API Key
            surl = shortener.bitly.short(lurl)
        elif type == "tinyurl":
            shortener = pyshorteners.Shortener()
            surl = shortener.tinyurl.short(lurl) 
        elif type == "qr":
            img = qrcode.make(lurl)
            img.save("static/qrcode.png")
            return render_template("qrcode.html")
        else:
            return render_template('error.html')
        
        return render_template('url.html', surl=surl)

@app.route("/imagetools", methods=["GET", "POST"])
def imagetools():
    if request.method == "GET":
        return render_template("imageinput.html")
    else:
        if "file" not in request.files:
            return render_template("error.html")
        
        file = request.files["file"]
        file_name = secure_filename(file.filename)
        if not allowed_file(file_name):
            return render_template("error.html")
        
        type = request.form.get("type")
        if not type or type not in ALLOWED_EXTENSIONS:
            return render_template("error.html")

        file.save(os.path.join(app.config['UPLOAD_FOLDER'], f"{type}.png"))
        return redirect("/")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS