from multiprocessing import current_process
import sqlite3
from contextlib import closing

def dict_factory(connection, row) -> dict:
    return {
            col[0]: row[idx] 
            for idx, col in enumerate(connection.description)
    }

def get_posts(connection:sqlite3.Connection) -> list[dict]:
    # connection.row_factory = sqlite3.Row
    connection.row_factory = dict_factory
    
    with closing(connection.cursor()) as cur:
        cursor = cur.execute(
            '''
            SELECT post_title, post_text, user_id
            FROM posts
            '''
        )
        return [row for row in cursor.fetchall()]


def insert_post(connection:sqlite3.Connection, post:dict):
    with closing(connection.cursor()) as cur:
        cur.execute(
            '''
            INSERT INTO posts
            (post_title, post_text, user_id)
            VALUES
            (:post_title, :post_text, :user_id)
            ''',
            post
        )

if __name__ == '__main__':
    connection = sqlite3.connect('social.db')

    # test_post = {
        # 'post_title': 'first post',
        # 'post_text': 'another this is a test',
        # 'user_id': 1
    # }
# 
    # insert_post(connection, test_post)
    print(get_posts(connection))
