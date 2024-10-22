from flask import Blueprint, jsonify, request, session, redirect, url_for, render_template

from models import Comment, Post, User, db, Publication

likes = Blueprint('likes', __name__)

@likes.route('/get_likes', methods=["GET"])
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

@likes.route('/like_post', methods=["POST"])
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
    return jsonify({"success": True, "likes" : post.likes}), 200

@likes.route('/likes')
def liked_page():
    name = session.get("username" , "")
    print(name)
    if name == "":
        return redirect(url_for('main_routes.login'))
    user = db.session.query(User).filter_by(name=name).first()
    if not user:
        return redirect(url_for('main_routes.login'))
    return render_template('likes.html', posts = user.get_liked_posts())

@likes.route('/like_pub', methods=["POST"])
def like_pub():
    name = session.get("username", "")
    post_id = request.form.get("post_id", "")
    if name == "" or post_id == "":
        raise Exception("Invalid request")
    user = db.session.query(User).filter_by(name=name).first()
    if not user:
        raise Exception("User not found")
    post = db.session.query(Publication).filter_by(id=post_id).first()
    if not post:
        raise Exception("Publication not found")
    user.like_pub(post)
    return jsonify({"success": True, "likes" : post.likes}), 200



