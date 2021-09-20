import os
from bottle import route, run
from datetime import datetime
import collections
import mysql.connector.pooling

BlogPost = collections.namedtuple('BlogPost', 'posted_at title content')

connection_pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name = "dbpool",
    pool_size = 5,
    host = 'gcp-snd-school-of-code-cloudsql-01-cloudsql.de.gcp.springernature.cloud',
    user = 'schoolofcode',
    password = 'schoolofcode',
    database = 'schoolofcode')

def get_blog_posts():
    with connection_pool.get_connection() as db_connection:
        with db_connection.cursor() as cursor:
            cursor.execute(("SELECT title, post_date, content FROM [INSERT HERE]"))

            posts = []
            for (title, post_date, content) in cursor:
                posts.append(BlogPost(posted_at=post_date.isoformat(), title=title, content=content))

            return posts


@route('/blog/posts')
def blog_posts():
    return {
        "posts": [post._asdict() for post in get_blog_posts()]
    }

@route('/')
def index():
    return '<p>Hello, web world!</p>'

@route('/hello/<name>')
def hello(name):
    return {
        "hello": name
    }

run(host='0.0.0.0', port=os.getenv('PORT', 8080))
