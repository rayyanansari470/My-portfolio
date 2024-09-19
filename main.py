from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import json
from flask_mail import Mail

with open("config.json", "r") as j:
    params = json.load(j)["params"]

local_server = True

app = Flask(__name__)

app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = params['gmail-user'],
    MAIL_PASSWORD = params['gmail-password']
)
mail = Mail(app)

if local_server:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']

db = SQLAlchemy(app)

class Contacts(db.Model):
    """
    sno name email phone_num msg
    """
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(25), nullable=False)
    phone_num = db.Column(db.String(15), nullable=False)
    msg = db.Column(db.String(150), nullable=False)

@app.route("/")
def home():
    return render_template("index.html", params = params)

@app.route("/about.html")
def about():
    return render_template("about.html", params = params)

@app.route("/resume.html")
def resume():
    return render_template("resume.html",params = params)

@app.route("/index.html")
def back():
    return render_template("index.html", params = params)

@app.route("/contact.html", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        """
        Add entry to database
        """
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        message = request.form.get("message")

        """
        sno name email phone_num msg
        """
        entry = Contacts(name=name, email=email, phone_num=phone, msg=message)
        db.session.add(entry)
        db.session.commit()
        mail.send_message('New message from' + name,
                          sender = email,
                          recipients = [params['gmail-user']],
                          body = message + "\n" + phone)
    return render_template("contact.html", params = params)

if __name__ == "__main__":
    app.run(debug=True)
