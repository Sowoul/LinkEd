from flask import Blueprint, jsonify, request, session

from models import Comment, Post, User, db

connections = Blueprint('connections', __name__)



@connections.route('/get_connections' , methods=["GET"])
def get_conns():
    name = session.get("username" , "")
    existing = db.session.query(User).filter_by(name=name).first()
    if name == "" or not existing:
        raise Exception("Invalid Id")
    store=[{"name" : dude.name , "pfp" : dude.pfp} for dude in existing.connections.all()]
    return store


@connections.route('/add_connection', methods=["POST"])
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


