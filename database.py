from multiprocessing import current_process
import sqlite3
from contextlib import closing


def get_posts(connection:sqlite3.Connection) -> list[tuple]:
    with closing(connection.cursor()) as cur:
        cursor = cur.execute(
            '''
            SELECT post_title, post_text, user_id
            FROM posts
            '''
        )
        return cursor.fetchall()


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
