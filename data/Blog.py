import uuid
import datetime
from data.Post import Post
from database import Database


class Blog:
    def __init__(self, author, title, description, id=uuid.uuid4().hex):
        self.author = author
        self.title = title
        self.description = description
        self.id = id

    def new_post(self):
        title = input('Enter title of post: ')
        content = input('Enter content of post: ')
        date = input('Enter date of post(DD-MM-YYYY) or leave blank for today: ')
        if date == '':
            date = datetime.datetime.utcnow()
        else:
            date = datetime.datetime.strptime(date, '%d-%m-%Y')
        post = Post(blog_id=self.id,
                    title=title,
                    content=content,
                    author=self.author,
                    date=date)
        post.save_to_mongo()

    def get_post(self):
        return Post.get_posts_from_mongo_by_blog_id(blog_id=self.id)

    def save_to_mongo(self):
        Database.insert(collection='blogs', data=self.json())

    def json(self):
        return {
            'author': self.author,
            'title': self.title,
            'description': self.description,
            'id': self.id
        }

    @classmethod
    def from_mongo(cls, id):
        blog_data = Database.find_one(collection='blogs', query={'id': id})
        return cls(author=blog_data['author'],
                   title=blog_data['title'],
                   description=blog_data['description'],
                   id=blog_data['id'])
