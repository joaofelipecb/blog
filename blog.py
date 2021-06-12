from flask import (
        Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from blog.db import get_db

bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    db = get_db()
    cur = db.cursor()
    cur.execute(
'''select post_id, post_title, post_body, post_created,
          user_id, user_username
   from posts
   natural join users
   order by post_created desc'''
    )
    posts = cur.fetchall()
    cur.close()
    return render_template('blog/index.html', posts=posts)
