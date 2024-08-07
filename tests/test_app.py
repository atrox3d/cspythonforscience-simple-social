from contextlib import closing
import sqlite3
from sqlite3 import Connection
from typing import Generator
import pytest
from fastapi.testclient import TestClient
from pathlib import Path

from database import get_posts, insert_post
from models import Post, Posts
# from app import app, connection as app_conn
import app

@pytest.fixture
def db_path() -> str:
    return 'test.db'

@pytest.fixture
def table_name() -> str:
    return 'posts'

@pytest.fixture
def connection(db_path:str) -> Generator[Connection, None, None]:
    print(f'CONNECTION | connecting to {db_path=}')
    conn =  sqlite3.connect(db_path)
    print(f'CONNECTION | yielding {conn=}')
    yield conn
    print(f'CONNECTION | closing {conn=}')
    conn.close()

@pytest.fixture
def empty_db_connection(app_connection: Connection,  table_name:str,  create_posts_table_sql:str) -> Generator[sqlite3.Connection, None, None]:
    with app_connection:
        with closing(app_connection.cursor()) as cur:
            print(f'EMPTY_DB_CONNECTION | dropping {table_name=}')
            cur.execute('DROP TABLE IF EXISTS posts')
            print(f'EMPTY_DB_CONNECTION | creating {table_name=}')
            cur.execute(create_posts_table_sql)
    yield app_connection

@pytest.fixture
def create_posts_table_sql() -> str:
    with open('migrations/step1.create_post_table.sql') as fp:
        return fp.read()

@pytest.fixture
def app_connection(connection: Connection) -> Generator[Connection, None, None]:
    # global app_conn
    app.connection = connection
    yield app.connection

@pytest.fixture
def test_post() -> Post:
    return Post(
        post_title='tenting post title',
        post_text='testing post text',
        user_id=0
    )

@pytest.fixture
def client():
    return TestClient(app.app)

@pytest.mark.xfail(reason='page changes dynamically')
def test_static_home(client):
    response = client.get('/')
    assert response.status_code == 200
    print(response.text)
    assert '<h1>simple social</h1>' in response.text

    with open('templates/index.html') as fp:
        html = fp.read()
    assert response.text == html

def test_app_connection(app_connection: Connection, db_path: str):
    print(f'TEST_APP_CONNECTION | start')
    for id_, name, filename in app_connection.execute('PRAGMA database_list'):
        if name == 'main' and filename is not None:
            path = filename
            break
    print(f'TEST_APP_CONNECTION | {path=}')
    assert Path(path).name == db_path

def test_no_posts(empty_db_connection: Connection):
    posts = get_posts(empty_db_connection)
    print(posts)
    assert posts == Posts(posts=[])

def test_one_post(empty_db_connection:Connection, test_post:Post):
    insert_post(empty_db_connection, test_post)
    posts = get_posts(empty_db_connection)
    print(posts)
    assert posts == Posts(posts=[test_post])

