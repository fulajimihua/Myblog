from App.exts import db


# 分类
class Classfy(db.Model):
    class_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    class_name=db.Column(db.String(100),unique=True)
    class_name2=db.Column(db.String(100))
    class_keywords=db.Column(db.String(100))
    class_description = db.Column(db.String(1000))


class Artical(db.Model):
    artical_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    artical_title=db.Column(db.String(100), unique=True)
    artical_content=db.Column(db.Text())
    artical_keywords=db.Column(db.String(100))
    art_descrip=db.Column(db.Text())
    artical_tag=db.Column(db.String(100))
    class_id=db.Column(db.Integer, db.ForeignKey(Classfy.class_id))
    clsfy=db.relationship('Classfy', backref='articals',lazy=True)

class Login(db.Model):
    login_times = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ip = db.Column(db.String(20))
    login_time = db.Column(db.DateTime())





