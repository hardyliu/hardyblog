import os
from dotenv import load_dotenv
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir,'.env'))

class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY','you-will-never-guess')
    
    #print('secretkey',SECRET_KEY)
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL','sqlite:///' + os.path.join(basedir, 'app.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    BLOG_POST_PER_PAGE = 10 #每页显示十条
    
    BLOG_MANAGE_POST_PER_PAGE = 15 #管理页面每页显示数
    BLOG_COMMENT_PER_PAGE = 15 #评论每页显示
    #配置邮件服务
    MAIL_SERVER = os.environ.get('MAIL_SERVER')    
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    
    ADMINS = [os.environ.get('ADMINS')]
    LANGUAGES = ['zh', 'en']
    #配置全文检索
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
    
    #换肤
    BLOG_THEMES = {'perfect_blue': 'Perfect Blue', 'black_swan': 'Black Swan'}