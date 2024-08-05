import sqlite3
from sqlite3 import Connection
from typing import Generator
from pathlib import Path
import pytest
from contextlib import closing

from database import get_posts, insert_post, dict_factory
from models import Post, Posts


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
def empty_db_connection(connection: Connection,  table_name:str,  create_posts_table_sql:str) -> Generator[sqlite3.Connection, None, None]:
    with connection:
        with closing(connection.cursor()) as cur:
            print(f'EMPTY_DB_CONNECTION | dropping {table_name=}')
            cur.execute('DROP TABLE IF EXISTS posts')
            print(f'EMPTY_DB_CONNECTION | creating {table_name=}')
            cur.execute(create_posts_table_sql)
    yield connection

@pytest.fixture
def create_posts_table_sql() -> str:
    with open('migrations/step1.create_post_table.sql') as fp:
        return fp.read()

@pytest.fixture
def test_post() -> Post:
    return Post(
        post_title='tensting post title',
        post_text='tensting post text',
        user_id=0
    )

def test_sql_fixture(empty_db_connection: Connection):
    print('START TEST')
    assert isinstance(empty_db_connection, Connection)

def test_insert_post(empty_db_connection:Connection, test_post:Post):
    insert_post(empty_db_connection, test_post)
    posts: Posts = get_posts(empty_db_connection)
    assert posts.posts == [test_post]

def test_get_posts(connection, test_post):
    insert_post(connection, test_post)
    posts: Posts = get_posts(connection)
    assert posts.posts == [test_post, test_post]
