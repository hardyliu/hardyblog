from flask import Flask
from flask_login import current_user
from hardyblog.extensions import  bootstrap, db, login_manager, moment, migrate,csrf
import click
from hardyblog.fakes import fake_admin, fake_categories, fake_posts, fake_comments
from hardyblog.models import Admin, Post, Category, Comment, Link
from config import Config

def create_app(config_name=Config):
    
    app = Flask('hardyblog') 
    app.config.from_object(config_name)
    #注册插件
    register_extensions(app)
    #注册蓝图
    register_blueprints(app)
    register_template_context(app)
    register_commands(app)
    return app


def register_blueprints(app):
    from hardyblog.blueprints.blog import blog_bp
    app.register_blueprint(blog_bp)
    from hardyblog.blueprints.auth import auth_bp
    app.register_blueprint(auth_bp)
    from hardyblog.blueprints.admin import admin_bp
    app.register_blueprint(admin_bp,url_prefix='/admin')

#注册插件    
def register_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    moment.init_app(app)
    migrate.init_app(app, db)
    
#注册模板上下文变量    
def register_template_context(app):
    @app.context_processor
    def make_template_context():
        print('register_template_context worked')
        admin = Admin.query.first()
        categories = Category.query.order_by(Category.name).all()
        links = Link.query.order_by(Link.name).all()
        if current_user.is_authenticated:
            unread_comments = Comment.query.filter_by(reviewed=False).count()
        else:
            unread_comments = None
        return dict(
            admin=admin, categories=categories,
            links=links, unread_comments=unread_comments)  
            
def register_commands(app):
    
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initDB(drop):
        """Initialize the database."""
        if drop:
            click.confirm('This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo('Drop tables.')
        db.create_all()
        click.echo('Initialized database.')
        
   
    
    
    @app.cli.command
    @click.option('--username', prompt=True, help='The username used to login.')
    @click.option('--password', prompt=True, hide_input=True,
                  confirmation_prompt=True, help='The password used to login.')
    def admin(username, password):
        """Building blog admin account, just for you."""

        click.echo('Initializing the database...')
        db.create_all()

        admin = Admin.query.first()
        if admin is not None:
            click.echo('The administrator already exists, updating...')
            admin.username = username
            admin.set_password(password)
        else:
            click.echo('Creating the temporary administrator account...')
            admin = Admin(
                username=username,
                blog_title='CoolBlog',
                blog_sub_title="No, I'm the real thing.",
                name='Admin',
                about='Anything about you.'
            )
            admin.set_password(password)
            db.session.add(admin)
        click.echo('Done.')
   
    @app.cli.group()
    def forge():
        pass
        
    @forge.command()
    @click.option('--category', default=10, help='Quantity of categories, default is 10.')
    @click.option('--post', default=50, help='Quantity of posts, default is 50.')
    @click.option('--comment', default=500, help='Quantity of comments, default is 500.')
    def content(category, post, comment):
        db.drop_all()
        db.create_all()   
        click.echo('Initializing the content for blog...')
        fake_admin()
        fake_categories()
        click.echo('categories has faked')
        fake_posts()
        click.echo('post has faked')
        fake_comments()
        click.echo('comments has faked')
        click.echo('Done.')