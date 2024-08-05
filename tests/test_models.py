import pytest
from models import Post, Posts


@pytest.fixture
def post_json(post: Post) -> dict:
    return post.model_dump()

@pytest.fixture
def post() -> Post:
    post = Post(
                    post_title='title',
                    post_text='text',
                    user_id=0
                )
    return post

@pytest.fixture
def ten_posts(post: Post) -> list[Post]:
    return [post for _ in range(10)]


def test_post_attributes(post: Post):
    assert post.post_title == 'title'
    assert post.post_text == 'text'
    assert post.user_id == 0

def test_post_json_attributes(post_json: dict):
    assert post_json['post_title'] == 'title'
    assert post_json['post_text'] == 'text'
    assert post_json['user_id'] == 0

def test_post_to_string(post:Post):
    assert str(post) == "post_title='title' post_text='text' user_id=0"

def test_post_to_repr(post: Post):
    assert repr(post) == "Post(post_title='title', post_text='text', user_id=0)"

def test_post_equality(post: Post):
    assert post == Post(
        post_text='text',
        post_title='title',
        user_id=0
    )
