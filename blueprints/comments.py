from flask import Blueprint, jsonify, request, session

from models import Comment, Post, User, db, Publication

comms = Blueprint('comms', __name__)

@comms.route('/add_comment', methods=["POST"])
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

@comms.route('/get_comments/<post_id>', methods=["GET"])
def get_comms(post_id):
    name = session.get("username" , "")
    if not name or not post_id:
        raise Exception("Invalid request")
    ref_post = db.session.query(Post).filter_by(id=post_id).first()
    if not ref_post:
        raise Exception("Post does not exist")
    return jsonify([comm.to_dict() for comm in  ref_post.comments.all()]), 200


@comms.route('/add_comment_pub', methods=["POST"])
def add_com_pub():
    name=session.get("username","")
    post_id = request.form.get("post_id","")
    content = request.form.get("comment","")
    print(name, post_id, content)
    if not name or not post_id or not content:
        raise Exception("Invalid request")
    user = db.session.query(User).filter_by(name=name).first()
    post = db.session.query(Publication).filter_by(id=post_id).first()
    post.add_comment(user,content)
    return jsonify(success=True) ,200