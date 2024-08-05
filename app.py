from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlite3 import Connection, Row

from database import get_posts, dict_factory, insert_post
from models import Post, Posts

app = FastAPI()
connection = Connection('social.db')
connection.row_factory = dict_factory

templates = Jinja2Templates(directory='templates')


@app.get('/')
async def home(request: Request) -> HTMLResponse:
    ''' home page '''

    context = get_posts(connection).model_dump()
    return templates.TemplateResponse(
        request=request,
        name='index.html',
        context=context
    )

@app.get('/posts')
async def posts():
    ''' get all posts '''
    return get_posts(connection)

@app.post('/posts')
async def posts(post:Post) -> Post:
    ''' add a post '''
    insert_post(connection, post)
    return post


