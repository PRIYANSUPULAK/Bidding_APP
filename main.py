from flask import Flask ,  render_template, url_for, request, redirect, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from users import User, Base

app = Flask(__name__)

engine = create_engine('sqlite:///advaitaUsers.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/',methods=['GET', 'POST'])
def home():
    return render_template('homePage.html')


@app.route('/login',methods=['GET', 'POST'])
def loginPage():
    if request.method=='POST':
        username=request.form["name"]
        password=request.form["pass"]
        if username is None or password is None:
            return redirect(url_for("loginPage"))
        user=session.query(User).filter_by(username=username).first()
        if not user or not user.verify_password(password):
            flash("wrong username or password")
            return redirect(url_for("loginPage"))
        flash("Welcome")
        return redirect(url_for("home"))

    else:
        return render_template('login.html')

@app.route('/signup',methods=['GET', 'POST'])
def signUpPage():
    if request.method == 'POST':
        username=request.form["name"]
        password=request.form["pass"]
        if username is None or password is None:
            return redirect(url_for("signUpPage"))
        if session.query(User).filter_by(username = username).first() is not None:
            flash("user already exits")
            return redirect(url_for("signUpPage"))
        user=User(username=username)
        user.hash_password(password)
        session.add(user)
        session.commit()
        flash("New Id Created!")
        return redirect(url_for("home"))
    else:
        return render_template('signUp.html')





if __name__ == '__main__':
    app.secret_key = 'secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
