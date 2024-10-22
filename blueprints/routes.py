import cloudinary
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
from flask import (Blueprint, jsonify, redirect, render_template, request,
                   session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash

from models import Comment, Post, User, connections, db

main_routes = Blueprint('main_routes', __name__)

cloudinary.config( 
    cloud_name = "dozuzq97z", 
    api_key = "837641246728126", 
    api_secret = "pxwX-qu7seTGZB_5p6IAaH_lKzU",
    secure=True
)

@main_routes.route('/')
def reds():
    temp = session.get("username", "")
    if temp == "":
        return redirect(url_for('main_routes.login'))
    return redirect(url_for('main_routes.home'))



@main_routes.route('/login', methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        name = request.form.get("username", "").lower()
        password = request.form.get("password", "")
        existing = db.session.query(User).filter_by(name=name).first()
        if not existing:
            return render_template('login.html', error="The user does not exist")
        if not check_password_hash(existing.getpass(), password):
            return render_template('login.html', error="The username and password do not match")
        session["username"] = name
        return redirect(url_for('main_routes.home'))
    return render_template('login.html')



@main_routes.route('/signup', methods=["GET", "POST"])
def signup():
    session.clear()
    if request.method == "POST":
        name = request.form.get("username", "").lower()
        password = request.form.get("password", "")
        pfp=request.form.get("pfp","")
        if name == "" or password == "":
            return render_template("signup.html", error="The username or password can't be null")
        if db.session.query(User).filter_by(name=name).first() is not None:
            return render_template("signup.html", error="The entered user exists!")
        hash = generate_password_hash(password)
        if pfp=="":
            newuser = User(name, hash)
        else:
            newuser = User(name, hash, pfp)
        db.session.add(newuser)
        db.session.commit()
        return redirect(url_for('main_routes.login'))
    return render_template('signup.html')



@main_routes.route('/home')
def home():
    name = session.get("username", "")
    existing = db.session.query(User).filter_by(name=name).first()
    if name == "" or not existing:
        return redirect(url_for('main_routes.login'))
    return render_template('index.html', name=name)

@main_routes.route('/get_connections' , methods=["GET"])
def get_conns():
    name = session.get("username" , "")
    existing = db.session.query(User).filter_by(name=name).first()
    if name == "" or not existing:
        raise Exception("Invalid Id")
    store=[{"name" : dude.name , "pfp" : dude.pfp} for dude in existing.connections.all()]
    return store


@main_routes.route('/add_connection', methods=["POST"])
def add_conn():
    name = session.get("username","")
    to_connect = request.form.get("to_connect","")
    if name=="" or to_connect == "":
        raise Exception('Wrong user')
    existing_og = db.session.query(User).filter_by(name=name).first()
    existing_tc = db.session.query(User).filter_by(name=to_connect).first()
    if not existing_og or not existing_tc:
        raise Exception('invalid request')
    existing_og.connect(existing_tc)
    return jsonify(success=True),200



@main_routes.route("/profile/", defaults={'name': None})
@main_routes.route("/profile/<name>")
def profile(name):
    isown=False
    if not name:
        name=session.get("username","")
    if name==session.get("username"):
        isown=True
    existing = db.session.query(User).filter_by(name=name).first()
    if not existing:
        raise Exception('invalid user')
    postos = existing.get_posts()
    pubs = existing.get_pubs()
    return render_template('profile.html' , posts=[postos[i].to_dict() for i in range(len(postos)-1,-1,-1)], user=existing.to_dict(), isown=isown, publications=[pubs[i].to_dict() for i in range(len(pubs)-1,-1,-1)] )

@main_routes.route('/likes')
def liked_page():
    name = session.get("username" , "")
    print(name)
    if name == "":
        return redirect(url_for('main_routes.login'))
    user = db.session.query(User).filter_by(name=name).first()
    if not user:
        return redirect(url_for('main_routes.login'))
    return render_template('likes.html', posts = user.get_liked_posts())