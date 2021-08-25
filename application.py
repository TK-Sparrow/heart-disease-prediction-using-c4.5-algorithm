import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from C4_5 import *

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class UserDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    email = db.Column(db.Text)
    password = db.Column(db.Text)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def __repr__(self):
        return f'''{self.name}, {self.password}, {self.email}'''


@app.route('/')
def index():
    db.create_all()
    return render_template('index.html')


@app.route('/login or signup')
def loginorsignup():
    return render_template('Login or Signup.html', uName="", email="", opass="", cpass="", lemail="", lpass="",
                           alert=False,
                           loginalert=False)


@app.route('/login')
def login():
    loginalert = False
    email = request.args.get('loginEmail')
    password = request.args.get('loginPassword')
    user = UserDetails.query.filter_by(email=email).first()
    print(user, email)
    if user:
        if user.password == password:
            return redirect(url_for('CalculateOpen'))
        else:
            loginalert = "Incorrect Password"
    else:
        loginalert = "User Not found"
    return render_template('Login or Signup.html', uName="", email="", opass="", cpass="", lemail="", lpass="",
                           alert=False, loginalert=loginalert)


@app.route('/register')
def SignUp():
    userName = request.args.get('userName')
    email = request.args.get('email')
    password = request.args.get('password')
    confirmPassword = request.args.get('cpassword')
    user = False
    user = UserDetails.query.filter_by(email=email).first()
    if user:
        alert = "Email Id is already registered. Try with other mail Id"
        return render_template('Login or Signup.html', uName=userName, email=email, opass=password,
                               cpass=confirmPassword, alert=alert)
    elif len(userName) < 4:
        alert = "User Name is to short"
        return render_template('Login or Signup.html', uName=userName, email=email, opass=password,
                               cpass=confirmPassword, alert=alert)
    elif len(password) < 8:
        alert = "Password Length is to short"
        return render_template('Login or Signup.html', uName=userName, email=email, opass=password,
                               cpass=confirmPassword, alert=alert)
    elif password != confirmPassword:
        alert = "Password and comfirm password are not matching"
        return render_template('Login or Signup.html', uName=userName, email=email, opass=password,
                               cpass=confirmPassword, alert=alert)
    newUser = UserDetails(userName, email, password)
    db.session.add(newUser)
    db.session.commit()

    return render_template('Login or Signup.html', uName="", email="", opass="", cpass="", lemail="", lpass="",
                           alert=False,
                           loginalert=False)


@app.route('/CalculateOpen')
def CalculateOpen():
    return render_template('calculate.html')


@app.route('/Calculate')
def Calculate():
    age = request.args.get('age')
    gender = request.args.get('gender')
    cp = request.args.get('cp')
    trestbps = request.args.get('trestbps')
    chol = request.args.get('chol')
    fbs = request.args.get('fbs')
    restecg = request.args.get('restecg')
    thalach = request.args.get('thalach')
    exang = request.args.get('exang')
    oldpeak = request.args.get('oldpeak')
    slope = request.args.get('slope')
    ca = request.args.get('ca')
    thal = request.args.get('thal')
    re = predecto([age, gender, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal])
    result = False
    if re == 0:
        result = False
    else:
        result = True
    return render_template('result.html', result=result)


if __name__ == '__main__':
    app.run()
