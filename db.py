# encoding=utf-8

import sys
reload(sys)
sys.setdefaultencoding("utf8")

from app import app
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:q1w2e3r4@localhost/wipweb'
db = SQLAlchemy(app)


def as_dict(model):
	result = {}
	for c in model.__table__.columns:
		key, value = c.name, getattr(model, c.name)
		if isinstance(value, datetime):
			result[key] = str(value)
		else:
			result[key] = value
	return result


class User(db.Model):
	id              = db.Column(db.Integer, primary_key=True)  # 用户ID
	username        = db.Column(db.String(128))                # 用户名
	password_hash   = db.Column(db.String(128))                # hash之后的密码
	chinese_name    = db.Column(db.String(128))                # 中文姓名
	name_in_paper   = db.Column(db.String(128))                # 论文中使用的名字
	alias           = db.Column(db.String(128))                # 别名(会出现在个人页面网址后缀中)
	gender          = db.Column(db.String(128))                # 性别: 男/女
	group           = db.Column(db.String(128))                # 组别: intern/master/doctor/faculty
	photo_url       = db.Column(db.String(1024))               # 头像URL
	enrollment_year = db.Column(db.Integer)                    # 入学年份
	graduation_year = db.Column(db.Integer)                    # 毕业年份
	introduction    = db.Column(db.Text)                       # 个人介绍

	def __init__(self, args=None):
		if args != None:
			self.update(args)

	def update(self, args):
		self.username        = args['username']
		self.password_hash   = args['password_hash']
		self.chinese_name    = args['chinese_name']
		self.name_in_paper   = args['name_in_paper']
		self.alias           = args['alias']
		self.gender          = args['gender']
		self.group           = args['group']
		self.photo_url       = args['photo_url']
		self.enrollment_year = args['enrollment_year']
		self.graduation_year = args['graduation_year']
		self.introduction    = args['introduction']


class Paper(db.Model):
	id              = db.Column(db.Integer, primary_key=True)  # 论文ID
	title           = db.Column(db.String(1024))               # 论文标题
	authors         = db.Column(db.String(1024))               # 论文作者(以英文逗号作为分隔符)
	publisher_name  = db.Column(db.String(128))                # 会议名称或期刊名称
	publisher_url   = db.Column(db.String(1024))               # 会议URL或期刊URL
	publish_type    = db.Column(db.String(128))                # 类别: 会议/期刊
	publish_year    = db.Column(db.Integer)                    # 发表年份
	pdf_url         = db.Column(db.String(1024))               # PDF文件URL

	def __init__(self, args=None):
		if args != None:
			self.update(args)

	def update(self, args):
		self.title          = args['title']
		self.authors        = args['authors']
		self.publisher_name = args['publisher_name']
		self.publisher_url  = args['publisher_url']
		self.publish_type   = args['publish_type']
		self.publish_year   = args['publish_year']
		self.pdf_url        = args['pdf_url']



class News(db.Model):
	id              = db.Column(db.Integer, primary_key=True)         # 新闻ID
	title           = db.Column(db.String(1024))                      # 新闻标题
	content         = db.Column(db.Text)                              # 新闻内容
	create_time     = db.Column(db.DateTime, default=datetime.now())  # 创建时间
	update_time     = db.Column(db.DateTime, default=datetime.now())  # 更新时间

	def __init__(self, args=None):
		if args != None:
			self.update(args)

	def update(self, args):
		self.title       = args['title']
		self.content     = args['content']
		self.update_time = datetime.now()


