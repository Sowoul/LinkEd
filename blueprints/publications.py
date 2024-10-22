import cloudinary
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
from flask import (Blueprint, jsonify, redirect, render_template, request,
                   session, url_for)

from models import Publication, User, db

publications = Blueprint("publications" , __name__ )
cloudinary.config( 
    cloud_name = "dozuzq97z", 
    api_key = "837641246728126", 
    api_secret = "pxwX-qu7seTGZB_5p6IAaH_lKzU",
    secure=True
)

@publications.route("/add_publication", methods=["POST"])
def add_publication():
    name = session.get("username", "")
    if name == "":
        return redirect(url_for('main_routes.login'))
    existing = db.session.query(User).filter_by(name=name).first()
    if not existing:
        return redirect(url_for('main_routes.login'))
    content = request.form.get("content", "")
    files = request.files.getlist("files")
    cloudinary_links = []
    for file in files:
        if file and allowed_file(file.filename):
            upload_result = upload(file)
            cloudinary_link, _ = cloudinary_url(upload_result['public_id'])
            cloudinary_links.append(cloudinary_link)
    if files:
        file_links = "|".join(cloudinary_links)
        existing.add_publication(file_links, content)
    else:
        existing.add_publication(content=content)
    return jsonify({'status': 'success', 'message': 'Post uploaded successfully!'})

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@publications.route('/publication/<pub_id>')
def redir_publication(pub_id):
    name=session.get("username" , "")
    if not name or not pub_id:
        raise Exception("Invalid request")
    post = db.session.query(Publication).filter_by(id=pub_id).first()
    if not post:
        return redirect(url_for('main_routes.home'))
    
    return render_template('publication.html', post=post.to_dict(), comments=[com.to_dict() for com in post.comments.all()])
