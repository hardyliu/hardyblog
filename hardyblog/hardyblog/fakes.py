import random

from faker import Faker
from hardyblog import db
faker = Faker('zh_CN')
from sqlalchemy.exc import IntegrityError
from hardyblog.models import Admin, Post, Category,Comment

#生成管理账号
def fake_admin():
    admin = Admin(
        username='admin',
        blog_title='Coolblog',
        blog_sub_title="No, I'm the real thing.",
        name='Mima Kirigoe',
        about='Um, l, Mima Kirigoe, had a fun time as a member of CHAM...'
    )
    admin.set_password('admin')
    db.session.add(admin)
    db.session.commit()

#模拟产生一些类别 
def fake_categories(count=10):
    category = Category(name='Default')
    db.session.add(category)

    for i in range(count):
        category = Category(name=faker.word())
        db.session.add(category)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()           
            
#模拟生成文章
def fake_posts(count=50):
    for i in range(count):
        post = Post(
            title = faker.sentence(),
            body = faker.text(1500),
            category = Category.query.get(random.randint(1,Category.query.count())),
            timestamp = faker.date_time_this_year()
        )
        db.session.add(post)
    db.session.commit()
    
    
def fake_comments(count=500):
    for i in range(count):
        comment = Comment(
            author=faker.name(),
            email=faker.email(),
            site=faker.url(),
            body=faker.sentence(),
            timestamp=faker.date_time_this_year(),
            reviewed=True,
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)

    salt = int(count * 0.1)
    for i in range(salt):
        # unreviewed comments
        comment = Comment(
            author=faker.name(),
            email=faker.email(),
            site=faker.url(),
            body=faker.sentence(),
            timestamp=faker.date_time_this_year(),
            reviewed=False,
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)

        # from admin
        comment = Comment(
            author='Mima Kirigoe',
            email='mima@example.com',
            site='example.com',
            body=faker.sentence(),
            timestamp=faker.date_time_this_year(),
            from_admin=True,
            reviewed=True,
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)
    db.session.commit()

    # replies
    for i in range(salt):
        comment = Comment(
            author=faker.name(),
            email=faker.email(),
            site=faker.url(),
            body=faker.sentence(),
            timestamp=faker.date_time_this_year(),
            reviewed=True,
            replied=Comment.query.get(random.randint(1, Comment.query.count())),
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)
    db.session.commit()    