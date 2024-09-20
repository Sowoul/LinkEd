from flask import (Blueprint, jsonify, redirect, render_template, request,
                   session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash

from models import Post, User, connections, db, Comment

import cloudinary
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url

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



@main_routes.route('/add_post', methods=["POST"])
def add_user_post():
    name = session.get("username", "")
    if name == "":
        return redirect(url_for('main_routes.login'))
    existing = db.session.query(User).filter_by(name=name).first()
    if not existing:
        return redirect(url_for('main_routes.login'))

    content = request.form.get("content", "")
    files = request.files.getlist("files")
    if not files:
        return jsonify({"error": "No files uploaded"}), 400

    cloudinary_links = []
    for file in files:
        if file and allowed_file(file.filename):
            upload_result = upload(file)
            cloudinary_link, _ = cloudinary_url(upload_result['public_id'])
            cloudinary_links.append(cloudinary_link)

    file_links = "|".join(cloudinary_links)
    existing.add_post(file_links, content)
    db.session.commit()

    return jsonify({'status': 'success', 'message': f'{len(cloudinary_links)} files uploaded'})

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@main_routes.route('/get_feed', methods=["GET"])
def get_user_feed():
    name = session.get("username", "")
    if name == "":
        return jsonify({"error": "Invalid user"}), 400

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 7, type=int)

    existing = db.session.query(User).filter_by(name=name).first()
    if not existing:
        return jsonify({"error": "User not found"}), 404

    paginated_posts = existing.get_feed(page=page, per_page=per_page)
    posts = [post.to_dict() for post in paginated_posts.items]

    return jsonify({
        "posts": posts,
        "total_pages": paginated_posts.pages,
        "current_page": paginated_posts.page,
        "has_next": paginated_posts.has_next
    }), 200

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
    return render_template('profile.html' , posts=[postos[i].to_dict() for i in range(len(postos)-1,-1,-1)], user=existing.to_dict(), isown=isown)

@main_routes.route('/get_likes', methods=["GET"])
def get_likes():
    name = session.get("username", "")
    post_id = request.args.get("post_id", "")
    if name == "" or post_id == "":
        raise Exception("Invalid request")
    user = db.session.query(User).filter_by(name=name).first()
    if not user:
        raise Exception("User not found")
    post = db.session.query(Post).filter_by(id=post_id).first()
    if not post:
        raise Exception("Post not found")
    return jsonify({"likes": post.likes}), 200

@main_routes.route('/like_post', methods=["POST"])
def like_post():
    name = session.get("username", "")
    post_id = request.form.get("post_id", "")
    if name == "" or post_id == "":
        raise Exception("Invalid request")
    user = db.session.query(User).filter_by(name=name).first()
    if not user:
        raise Exception("User not found")
    post = db.session.query(Post).filter_by(id=post_id).first()
    if not post:
        raise Exception("Post not found")
    user.like_post(post)
    db.session.commit()
    return jsonify({"success": True, "likes" : post.likes}), 200

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

@main_routes.route('/add_comment', methods=["POST"])
def add_com():
    name=session.get("username","")
    post_id = request.form.get("post_id","")
    content = request.form.get("comment","")
    print(name, post_id, content)
    if not name or not post_id or not content:
        raise Exception("Invalid request")
    user = db.session.query(User).filter_by(name=name).first()
    post = db.session.query(Post).filter_by(id=post_id).first()
    post.add_comment(user,content)
    return jsonify(success=True) ,200

@main_routes.route('/get_comments/<post_id>', methods=["GET"])
def get_comms(post_id):
    name = session.get("username" , "")
    if not name or not post_id:
        raise Exception("Invalid request")
    ref_post = db.session.query(Post).filter_by(id=post_id).first()
    if not ref_post:
        raise Exception("Post does not exist")
    return jsonify([comm.to_dict() for comm in  ref_post.comments.all()]), 200

@main_routes.route('/post/<post_id>')
def redir_post(post_id):
    name=session.get("username" , "")
    if not name or not post_id:
        raise Exception("Invalid request")
    post = db.session.query(Post).filter_by(id=post_id).first()
    if not post:
        return redirect(url_for('main_routes.home'))
    
    return render_template('post.html', post=post.to_dict(), comments=[com.to_dict() for com in post.comments.all()])