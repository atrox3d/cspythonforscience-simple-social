from fastapi import FastAPI
from sqlite3 import Connection, Row

from database import get_posts, dict_factory, insert_post
from models import Post, Posts

app = FastAPI()
connection = Connection('social.db')
connection.row_factory = dict_factory

@app.get('/')
async def root():
    return {'message': 'server running'}

@app.get('/posts')
async def posts():
    return get_posts(connection)

@app.post('/posts')
async def posts(post:Post) -> Post:
    insert_post(connection, post)
    return post


