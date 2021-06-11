from flask import (
        Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from blog.auth import login_required
from blog.db import get_db

bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
'''select post_id, post_title, post_body, post_created,
          user_id, user_username
   from post
   natural join user
   order by post_created desc'''
   )
    return render_template('blog/index.html', posts=posts)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'
        else:
            db = get_db()
            db.execute(
'''insert into post (post_title, post_body, user_id)
values (?, ?, ?)''',
            (title, body, g.user['id'])
            )
            return redirect(url_for('blog.index'))
        return render_template('blog/create.html')

def get_post(id, check_author=True):
    post = get_db().execute(
'''select post_id, post_title, post_body, post_created, user_id, user_username
from post
natural join user
where post_id = ?''').fetchone()
    
    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['user_id'] != g.user['user_id']:
        abort(403)

    return post

@bp.route('/<int:id>/update', methods=('GET','POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
'''update post set post_title = ?, body = ?
where id = ?''',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))
        return render_template('blog/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('delete from post where post_id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))

