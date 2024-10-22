import cloudinary
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
from flask import Blueprint, jsonify, redirect, request, session, url_for, render_template

from models import Comment, Post, User, db

posts = Blueprint('posts', __name__)

cloudinary.config( 
    cloud_name = "dozuzq97z", 
    api_key = "837641246728126", 
    api_secret = "pxwX-qu7seTGZB_5p6IAaH_lKzU",
    secure=True
)



@posts.route('/add_post', methods=["POST"])
def add_user_post():
    name = session.get("username", "")
    print(f'request from {name}')
    if name == "":
        return redirect(url_for('main_routes.login'))
    existing = db.session.query(User).filter_by(name=name).first()
    if not existing:
        return redirect(url_for('main_routes.login'))

    content = request.form.get("content", "")
    files = request.files.getlist("files")
    print('aaa')     
    cloudinary_links = []
    for file in files:
        if file and allowed_file(file.filename):
            upload_result = upload(file)
            cloudinary_link, _ = cloudinary_url(upload_result['public_id'])
            cloudinary_links.append(cloudinary_link)
    if files:
        file_links = "|".join(cloudinary_links)
        existing.add_post(file_links, content)
    else:
        existing.add_post(content=content)
    return jsonify({'status': 'success', 'message': 'Post uploaded successfully!'})

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@posts.route('/get_feed', methods=["GET"])
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

@posts.route('/post/<post_id>')
def redir_post(post_id):
    name=session.get("username" , "")
    if not name or not post_id:
        raise Exception("Invalid request")
    post = db.session.query(Post).filter_by(id=post_id).first()
    if not post:
        return redirect(url_for('main_routes.home'))
    
    return render_template('post.html', post=post.to_dict(), comments=[com.to_dict() for com in post.comments.all()])


