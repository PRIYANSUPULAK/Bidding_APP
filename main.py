from flask import Flask ,  render_template, url_for, request, redirect, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from users import User, Base, Item
from flask import session as login_session
from datetime import datetime, timedelta


app = Flask(__name__)

engine = create_engine('sqlite:///advaitaUsers.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/<int:user_id>/new',methods=['GET', 'POST'])
def new(user_id):
    if 'username' not in login_session:
        return redirect('/login')
    if login_session['user_id']!=user_id:
        return redirect(url_for('home'))
    if request.method=='POST':
        name=request.form["name"]
        price=request.form["price"]
        description=request.form["description"]
        img=request.form["inputfile"]
        cur=datetime.now()
        s1=str(cur)
        cur2=cur+timedelta(hours=24)
        s2=str(cur2)
        item=Item(name=name, price=price, description=description, img=img, start_date=s1, end_date=s2, user_id=user_id)
        session.add(item)
        session.commit()
        return redirect(url_for("profile", user_id = user_id))

    else:
        return render_template('new.html',user_id=user_id)


@app.route('/<int:user_id>/')
def profile(user_id):
    if 'username' not in login_session:
        return redirect('/login')
    if login_session['user_id']!=user_id:
        return redirect(url_for('home'))
    user=session.query(User).filter_by(id=user_id).one()
    user_id=user.id
    items=session.query(Item).filter_by(user_id = user.id)
    #xyz=session.query(Item).filter_by(user_id = user.id).one()
    #print(xyz.img)
    return render_template('profile.html',user=user,items=items, user_id=user_id)

@app.route('/')
def home():
    if 'username' not in login_session:
        return redirect('/login')
    return redirect(url_for('auction'))

@app.route('/logout')
def logoutPage():
    del login_session['username']
    return redirect(url_for('auction'))


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
        login_session['username']=username
        user = session.query(User).filter_by(username=username).one()
        login_session['user_id']=user.id
        flash("Welcome")
        return redirect(url_for("auction"))

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
        return redirect(url_for("loginPage"))
    else:
        return render_template('signUp.html')

@app.route('/about')
def about():
    return "Visit Advaita website, Register there and let us welcome you on the Eve of Advaita"


@app.route('/bidding/<int:id>',methods=['GET','POST'])
def bidding(id):
    if 'username'  not in login_session:
        return redirect(url_for("loginPage"))
    if request.method=='POST':
        newPrice=int(request.form['newPrice'])
        tag = login_session['username']
        print(newPrice)
        print(type(newPrice))
        item=session.query(Item).filter_by(id=id).one()
        print(item.price)
        print(type(item.price))
        if item.price < newPrice:
            print("here")
            item.price=newPrice
            item.tag=tag
            session.add(item)
            session.commit()
        return redirect(url_for("auction"))

@app.route('/auction/')
def auction():
    items=session.query(Item).all()
    cur=datetime.now()
    cur=str(cur)
    if 'username' not in login_session:
        return render_template('publicauction.html',items=items, cur_date=cur)
    return render_template("auction.html", items=items, cur_date=cur,user_id = login_session['user_id'])

@app.route('/yourproducts')
def yourProducts():
    if 'username' not in login_session:
        return redirect(url_for("loginPage"))
    items=session.query(Item).all()
    username = login_session['username']
    return render_template("yourProducts.html",items=items, username=username, user_id = login_session['user_id'])



if __name__ == '__main__':
    app.secret_key = 'secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
