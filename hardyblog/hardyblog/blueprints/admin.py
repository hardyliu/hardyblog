from flask import Blueprint,url_for,redirect,render_template, flash,request,current_app
from flask_login import current_user,login_required
from hardyblog.forms import SettingsForm,PostForm,CategoryForm
from hardyblog.models import Admin, Post, Category,Comment
from hardyblog import db
from hardyblog.utils import redirect_back

admin_bp = Blueprint('admin', __name__)


#文章管理    
@admin_bp.route('/manage/post', methods=['GET'])
@login_required
def manage_post():
    page = request.args.get('page' , 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page=current_app.config['BLOG_POST_PER_PAGE'])
    posts = pagination.items
   
    return render_template('admin/post_manage.html', page=page, pagination=pagination, posts=posts)
#管理员发表文章
@admin_bp.route('/post', methods=['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post()
        post.title = form.title.data
        post.body = form.body.data
        post.category_id = form.category.data
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('.new_post'))
     
    return render_template('admin/new_post.html', form = form)
    
#编辑文章
@admin_bp.route('/post/<int:post_id>/edit', methods=['GET','POST'])
@login_required
def edit_post(post_id):
    form = PostForm()
    post = Post.query.get_or_404(post_id)
        
    if form.validate_on_submit():
        post.title = form.title.data
        post.category_id = form.category.data
        post.body = form.body.data
        db.session.commit()
        flash('Post updated','info')
        return redirect(url_for('.manage_post'))
    form.title.data = post.title
    form.category.data = post.category_id
    form.body.data = post.body
    return render_template('admin/edit_post.html', form = form)  
    
#删除指定文章
@admin_bp.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted.', 'success')
    return redirect(url_for('.manage_post'))  

#设置评论功能    
@admin_bp.route('/post/<int:post_id>/set-comment',methods=['POST'])
@login_required
def set_comment(post_id):
    post = Post.query.get_or_404(post_id)
    if post.can_comment:
        post.can_comment = False
        flash('Comment disabled.', 'success')
    else:
        post.can_comment = True
        flash('Comment enabled.', 'success')
        
    db.session.commit()
    return redirect_back()

 
#目录管理
@admin_bp.route('/manage/category', methods=['GET'])
@login_required
def manage_category():
    return render_template('admin/category_manage.html')   
    
#添类别    
@admin_bp.route('/category/new', methods=['GET','POST'])
@login_required
def new_category():
    form = CategoryForm()
    if form.validate_on_submit():       
        category = Category()
        category.name = form.name.data
        db.session.add(category)
        db.session.commit()
        flash('Category has build','success')
        return redirect(url_for('.manage_category'))
     
    return render_template('admin/new_category.html', form = form)
        

#类别修改
@admin_bp.route('/category/<int:category_id>/edit', methods=['GET','POST'])
@login_required
def edit_category(category_id):
    form = CategoryForm()
    category = Category.query.get_or_404(category_id)
    if category.id == 1:
        flash('You can not edit the default category.', 'warning')
        return redirect(url_for('blog.index'))
        
    if form.validate_on_submit():
        category.name = form.name.data
        db.session.commit()
        flash('Category updated','info')
        return redirect(url_for('.manage_category'))
    form.name.data = category.name    
    return render_template('admin/edit_category.html', form = form)  
    
#目录管理
@admin_bp.route('/category/<int:category_id>/delete', methods=['POST'])
@login_required
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    if category.id == 1:
        flash('You can not delete the default category.', 'warning')
        return redirect(url_for('blog.index'))
    category.delete()
    flash('Category removed.', 'success')
    return redirect(url_for('.manage_category'))        

#评论管理
@admin_bp.route('/manage/comment', methods=['GET'])
@login_required
def manage_comment():
    page = request.args.get('page', 1, type=int)
    type = request.args.get('type')
    if 'unread' == type:
        pagination = Comment.query.filter_by(reviewed=False).order_by(Comment.timestamp.desc()).paginate(page, per_page = current_app.config['BLOG_POST_PER_PAGE'])
    elif 'admin' == type:
        pagination = Comment.query.filter_by(from_admin=True).order_by(Comment.timestamp.desc()).paginate(page, per_page = current_app.config['BLOG_POST_PER_PAGE'])
    else:
        pagination = Comment.query.order_by(Comment.timestamp.desc()).paginate(page, per_page = current_app.config['BLOG_POST_PER_PAGE'])
    
    comments = pagination.items
    
    return render_template('admin/comment_manage.html', page=page, comments = comments, pagination = pagination)
    

@admin_bp.route('/comment/<int:comment_id>/approve', methods=['POST'])
@login_required
def approve_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    comment.reviewed = True
    db.session.commit()
    flash('Comment published.', 'success')
    return redirect_back()
    

@admin_bp.route('/comment/<int:comment_id>/delete',methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)  
    db.session.delete(comment)
    db.session.commit()
    flash('Comment deleted.', 'success')
    return redirect_back()
    

#博客基础信息设置
@admin_bp.route('/settings', methods=['GET','POST'])
@login_required
def settings():
    form = SettingsForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.blog_title = form.blog_title.data
        current_user.blog_sub_title = form.blog_sub_title.data
        current_user.about = form.about.data
        db.session.commit()
        flash('Setting updated.', 'success')
        return redirect(url_for('blog.index'))
    
    form.name.data = current_user.name
    form.blog_title.data= current_user.blog_title
    form.blog_sub_title.data = current_user.blog_sub_title
    form.about.data= current_user.about
    return render_template('admin/settings.html',form = form)                