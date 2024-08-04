from multiprocessing import current_process
import sqlite3
from contextlib import closing

from models import Post, Posts

def dict_factory(connection, row) -> dict:
    return {
            col[0]: row[idx] 
            for idx, col in enumerate(connection.description)
    }

def get_posts(connection:sqlite3.Connection) -> Posts:
    # connection.row_factory = sqlite3.Row
    connection.row_factory = dict_factory
    
    with connection:
        with closing(connection.cursor()) as cur:
            cursor = cur.execute(
                '''
                SELECT post_title, post_text, user_id
                FROM posts
                '''
            )
            return Posts(posts=[Post.model_validate(row) for row in cursor.fetchall()])
            # return [Post.model_validate(row) for row in cursor.fetchall()]


def insert_post(connection:sqlite3.Connection, post:Post):
    with connection:
        with closing(connection.cursor()) as cur:
            cur.execute(
                '''
                INSERT INTO posts
                (post_title, post_text, user_id)
                VALUES
                (:post_title, :post_text, :user_id)
                ''',
                post.model_dump()
            )
        # connection.commit()

if __name__ == '__main__':
    connection = sqlite3.connect('social.db')

    test_post = {
        'post_title': 'first pydantic post',
        'post_text': 'pydantic post',
        'user_id': 1
    }

    test_post = Post(**test_post)

    insert_post(connection, test_post)
    print(get_posts(connection))
