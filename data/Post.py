import uuid
import datetime

from database import Database


class Post:
    def __init__(self, blog_id, title, content, author,
                 date=datetime.datetime.utcnow(), id=uuid.uuid4().hex):
        self.content = content
        self.title = title;
        self.author = author
        self.blog_id = blog_id
        self.id = id
        self.created_date = date

    def save_to_mongo(self):
        Database.insert(collection='posts', data=self.json())

    def json(self):
        return {
            "blog_id": self.blog_id,
            "id": self.id,
            'title': self.title,
            'content': self.content,
            'author': self.content,
            'created_date': self.created_date
        }

    @classmethod
    def get_post_from_mongo(cls, id):
        post_data = Database.find_one(collection='posts', query={'id': id})
        return cls(blog_id=post_data['blog_id'],
                   title=post_data['title'],
                   content=post_data['content'],
                   author=post_data['author'],
                   date=post_data['created_date'],
                   id=post_data['id'])

    @staticmethod
    def get_posts_from_mongo_by_blog_id(blog_id):
        return [post for post in Database.find(collection='posts', query={'blog_id': blog_id})]
