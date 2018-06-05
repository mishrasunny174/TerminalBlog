from database import Database
from data.Blog import Blog


class Menu:
    def __init__(self):
        self.user = input("Enter your author name: ")
        self.user_blog = None
        if self._user_has_account():
            print('Welcome, {}'.format(self.user))
        else:
            self._prompt_for_new_account()

    def _user_has_account(self):
        blog = Database.find_one('blogs', {'author': self.user})
        if blog is not None:
            self.user_blog = Blog.from_mongo(blog[id])
            return True
        else:
            return False

    def _prompt_for_new_account(self):
        title = input('title: ')
        description = input('description: ')
        blog = Blog(author=self.user, title=title, description=description)
        blog.save_to_mongo()
        self.user_blog = blog

    def run_menu(self):
        while True:
            print('\n\n\n#### BLOG MENU ####')
            print('What do you wanna do?')
            print('1) Write a post in your blog')
            print('2) Read posts from blog')
            print('3) EXIT')
            choice = int(input('Enter your choice: '))
            if choice == 1:
                self.user_blog.new_post()
            elif choice == 2:
                self._show_all_blog()
                self._view_blog()
            elif choice == 3:
                print('Bye!')
                return
            else:
                print('ERROR: Wrong choice Try Again')

    def _show_all_blog(self):
        blogs = Database.find(collection='blogs', query={})
        for blog in blogs:
            print('ID: {}, Title: {}, Author: {}, Description: {}'.format(blog['id'],
                                                                          blog['title'],
                                                                          blog['author'],
                                                                          blog['description']))

    def _view_blog(self):
        blog_id = input('Enter blog id you want to read: ')
        blog = Blog.from_mongo(blog_id)
        posts = blog.get_post()
        for post in posts:
            print('Date: {}, Title: {}\n\n{}'.format(post['created_date'],
                                                     post['title'],
                                                     post['content']))
