from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import Thread, Post
from . import db

forum = Blueprint('forum', __name__)


@forum.route('/threads', methods=['GET', 'POST'])
@login_required
def threads():
    if request.method == 'POST':
        title = request.form.get('title')
        new_thread = Thread(title=title, user_id=current_user.id)
        db.session.add(new_thread)
        db.session.commit()
        return redirect(url_for('forum.threads'))
    threads = Thread.query.order_by(Thread.timestamp.desc()).all()
    return render_template('threads.html', threads=threads)


@forum.route('/thread/<int:id>', methods=['GET', 'POST'])
@login_required
def thread(id):
    thread = Thread.query.get_or_404(id)
    if request.method == 'POST':
        content = request.form.get('content')
        new_post = Post(content=content, user_id=current_user.id, thread_id=thread.id)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('forum.thread', id=id))
    posts = Post.query.filter_by(thread_id=thread.id).order_by(Post.timestamp.desc()).all()
    return render_template('thread.html', thread=thread, posts=posts)


@forum.route('/upvote/<int:id>')
@login_required
def upvote(id):
    post = Post.query.get_or_404(id)
    post.upvotes += 1
    db.session.commit()
    return jsonify(success=True, count=post.upvotes)


@forum.route('/downvote/<int:id>')
@login_required
def downvote(id):
    post = Post.query.get_or_404(id)
    post.downvotes += 1
    db.session.commit()
    return jsonify(success=True, count=post.downvotes)
