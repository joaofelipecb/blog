
from flask import (
        Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from blog.db import get_db

bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    import psycopg2.extras
    db = get_db()
    cur = db.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
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
