from flaskblog.models import Posts
from flaskblog.posts.forms import NewPost
from flaskblog import db
from flask import render_template, flash, redirect, url_for, request, abort, Blueprint
from flask_login import login_required, current_user

posts = Blueprint("posts", __name__)


@posts.route("/new_post", methods=['GET', 'POST'])
@login_required
def new_post():
    form = NewPost()
    if form.validate_on_submit():
        post = Posts(title=form.title.data,
                     content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('New Post created successfully', "success")
        return redirect(url_for("main.home"))
    return render_template('create_post.html', title='New Post', form=form, legend="New Post")


@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Posts.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Posts.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = NewPost()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Your post has been updated", "success")
        return redirect(url_for("posts.post", post_id=post.id))
    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
    return render_template("create_post.html", title="Update Post", form=form, legend="Update Post")


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Posts.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Your post has been deleted", "danger")
    return redirect(url_for("main.home"))
