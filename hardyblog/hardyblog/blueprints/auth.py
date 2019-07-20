from flask import Blueprint,flash,url_for,redirect,render_template,request
from hardyblog.models import Admin
from hardyblog.forms import AdminLoginForm
from flask_login import login_user, logout_user,current_user
from hardyblog.utils import redirect_back
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/auth/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('blog.index'))
        
    loginForm = AdminLoginForm()
  
    if loginForm.validate_on_submit():
        username = loginForm.username.data
        user = Admin.query.filter_by(username=username).first()
        if user is None or not user.validate_password(loginForm.password.data):
            flash('Sorry.Invalid username or password','warning')
            return redirect(url_for('.login'))
         
        login_user(user, remember=loginForm.remember.data)
        flash('Welcome back.', 'info')
        return redirect_back()
            
    return render_template('auth/login.html',form = loginForm)
    
@auth_bp.route('/auth/logout')    
def logout():
    logout_user()
    return  redirect_back()