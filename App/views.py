from flask import Blueprint, render_template, request, redirect, url_for, session
from App.models import *

blue = Blueprint('blog', __name__)


@blue.route('/',methods=['get','post'])
def choose():
    if request.method == 'GET':
        return render_template('admin/Choose.html')
    else:
        if request.form.get('usertype') == 'User':
            res = redirect(url_for('blog.index'))
        else:
            res = redirect(url_for('blog.admin_login'))
        return res

# 首页
@blue.route('/homepage/')
def index():
    classfys = Classfy.query.all()
    articals = Artical.query.all()
    for classfy in classfys:
        classfy.length=len(classfy.articals)
    return render_template('home/index.html',classfys=classfys,articals=articals)

@blue.route('/index/<c>/')
def index2(c):
    classfys=Classfy.query.all()
    articals = Classfy.query.get(c).articals
    for classfy in classfys:
        classfy.length=len(classfy.articals)
    return render_template('home/index.html', classfys=classfys, articals=articals)

@blue.route('/info/<a>/')
def info(a):
    artical = Artical.query.get(a)
    classfys = Classfy.query.all()
    for classfy in classfys:
        classfy.length=len(classfy.articals)
    return render_template('home/info.html',artical=artical,classfys=classfys)
# 后台
@blue.route('/admin/login/',methods=['post','get'])
def admin_login():
    if request.method == "GET":
        return render_template('admin/login.html')
    else:
        if request.form.get('username') == 'admin' and request.form.get('userpwd') == '12345678':
            res = redirect(url_for('blog.admin'))
            session['username'] = request.form.get('username')
            return res
        else:
            return redirect(url_for('blog.admin_login'))
#后台主页
@blue.route('/admin/')
def admin():
    # if request.cookies.get('session') == session['username']:
    if session.get('username',''):
        articles_num = Artical.query.count()
        return render_template('admin/index.html',articles_num=articles_num)
    else:
        return redirect(url_for('blog.admin_login'))

#文章
@blue.route('/admin/article/<int:page>/', methods=['get','post'])
def article2(page):
    if session.get('username',''):
        if request.method =='GET':
            articles = Artical.query.paginate(page, 4, False).items
            return render_template('admin/article.html', art=articles)
        else:
            article_ids = request.form.getlist('article_id')
            print(article_ids, type(article_ids))
            for id in article_ids:
                article = Artical.query.get(id)
                db.session.delete(article)
                db.session.commit()
            return redirect(url_for('blog.article2', page=1))
    else:
        return redirect(url_for('blog.admin_login'))


#栏目
@blue.route('/admin/category/', methods=['get','post'])
def category():
    if session.get('username',''):
        if request.method == 'GET':
            categorys = Classfy.query.order_by(Classfy.class_id).all()
            for category in categorys:
                category.length = len(category.articals)
            res = render_template('admin/category.html', categorys=categorys)
            return res
        else:
            name = request.form.get('name')
            name2 = request.form.get('alias')
            keywords = request.form.get('keywords')
            desicription = request.form.get('describe')
            classfy = Classfy()
            classfy.class_description = desicription
            classfy.class_keywords = keywords
            classfy.class_name2 = name2
            classfy.class_name = name
            db.session.add(classfy)
            db.session.commit()
            categorys = Classfy.query.order_by(Classfy.class_id).all()
            for category in categorys:
                category.length = len(category.articals)
            res = render_template('admin/category.html', categorys=categorys)
            return res
    else:
        return redirect(url_for('blog.admin_login'))


#删除分类
@blue.route('/admin/delcategory/')
def delcategory():
    if session.get('username',''):
        category_id = request.args.get('id')
        # print(category_id,type(category_id))
        category = Classfy.query.get(category_id)
        for article in category.articals:
            db.session.delete(article)
            db.session.commit()
        db.session.delete(category)
        db.session.commit()
        res = redirect(url_for('blog.category'))
        return res
    else:
        return redirect(url_for('blog.admin_login'))


#修改分类
@blue.route('/admin/updatecategory/',methods = ['get','post'])
def updatecategory():
    if session.get('username',''):
        if request.method == "GET":
            category = Classfy.query.get(request.args.get('id'))
            return render_template('admin/update-category.html', category=category)
        else:
            name = request.form.get('name')
            name2 = request.form.get('alias')
            keywords = request.form.get('keywords')
            desicription = request.form.get('describe')
            classfy = Classfy.query.get(request.form.get('id'))
            classfy.class_description = desicription
            classfy.class_keywords = keywords
            classfy.class_name2 = name2
            classfy.class_name = name
            db.session.commit()
            res = redirect(url_for('blog.category'))
            return res
    else:
        return redirect(url_for('blog.admin_login'))


#修改文章
@blue.route('/admin/updatearticle/',methods = ['get','post'])
def updatearticle():
    if session.get('username',''):
        if request.method == 'GET':
            article = request.args.get('article')
            return render_template('admin/update-article.html', article=Artical.query.get(article),
                                   categorys=Classfy.query.all())
        else:
            id = request.form.get('id')
            title = request.form.get('title')
            content = request.form.get('content')
            keywords = request.form.get('keywords')
            describe = request.form.get('describe')
            class_id = request.form.get('class_id')
            artical_tag = request.form.get('tag')
            article = Artical.query.get(id)
            article.artical_title = title
            article.artical_content = content
            article.artical_keywords = keywords
            article.art_descrip = describe
            article.class_id = class_id
            article.artical_tag = artical_tag
            db.session.commit()
            return redirect(url_for('blog.article2', page=1))
    else:
        return redirect(url_for('blog.admin_login'))


#增加文章
@blue.route('/admin/addarticle/',methods = ['get','post'])
def addarticle():
    if session.get('username',''):
        if request.method == 'GET':
            return render_template('admin/add-article.html', categorys=Classfy.query.all())
        else:
            id = request.form.get('id')
            title = request.form.get('title')
            content = request.form.get('content')
            keywords = request.form.get('keywords')
            describe = request.form.get('describe')
            class_id = request.form.get('class_id')
            artical_tag = request.form.get('tag')
            article = Artical()
            article.artical_title = title
            article.artical_content = content
            article.artical_keywords = keywords
            article.art_descrip = describe
            article.class_id = class_id
            article.artical_tag = artical_tag

            db.session.add(article)
            db.session.commit()
            return redirect(url_for('blog.article2', page=1))
    else:
        return redirect(url_for('blog.admin_login'))


#删除文章
@blue.route('/admin/deletearticle/')
def deletearticle():
    if session.get('username',''):
        article = request.args.get('article')
        article1 = Artical.query.get(article)
        db.session.delete(article1)
        db.session.commit()
        return redirect(url_for('blog.article2', page=1))
    else:
        return redirect(url_for('blog.admin_login'))

# 退出登录
@blue.route('/admin/logout/')
def logout():
    session.pop('username')
    res = redirect(url_for('blog.index'))
    return res
