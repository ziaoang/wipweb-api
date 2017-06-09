# encoding=utf-8

import sys
reload(sys)
sys.setdefaultencoding("utf8")


from flask import Flask, make_response, jsonify, g
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
import hashlib
from itsdangerous import TimedJSONWebSignatureSerializer, SignatureExpired, BadSignature


# Flask配置
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:webkdd@localhost/wipweb"
app.config["SECRET_KEY"] = "WIPWEB_SECRET_KEY"
app.config["UPLOAD_URL"] = "http://127.0.0.1:5000/static/upload/"


@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({"status" : "error", "message" : "页面无法找到"}), 404)


@app.after_request
def after_request(response):
	response.headers.add("Access-Control-Allow-Origin", "*")
	response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
	response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE")
	return response


db = SQLAlchemy(app)
auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(id, token):
	user = User.verify_auth_token(token)
	if not user:
		return False
	if user.id != int(id):
		return False
	g.user = user
	return True


@auth.error_handler
def auth_error():
	return jsonify({"status" : "error", "message" : "没有权限"})


# 用户表
class User(db.Model):
	id            = db.Column(db.Integer, primary_key=True)  # 用户ID
	username      = db.Column(db.String(128), unique=True)   # 账号
	password_hash = db.Column(db.String(128))                # 密码(hash后)
	alias         = db.Column(db.String(128), unique=True)   # 别名(会出现在个人页面网址后缀中)
	cn_name       = db.Column(db.String(128))                # 中文姓名
	en_name       = db.Column(db.String(128))                # 英文姓名
	cn_intro      = db.Column(db.Text)                       # 中文介绍
	en_intro      = db.Column(db.Text)                       # 英文介绍
	photo_url     = db.Column(db.String(1024))               # 头像URL
	group         = db.Column(db.String(128))                # 身份
	year          = db.Column(db.Integer)                    # 加入年份

	def generate_auth_token(self, expiration = 3600):
		s = TimedJSONWebSignatureSerializer(app.config["SECRET_KEY"], expires_in = expiration)
		return s.dumps({"id": self.id})

	def as_dict(self):
		out = {}
		out["id"]        = self.id
		out["username"]  = self.username
		out["alias"]     = self.alias
		out["cn_name"]   = self.cn_name
		out["en_name"]   = self.en_name
		out["cn_intro"]  = self.cn_intro
		out["en_intro"]  = self.en_intro
		out["photo_url"] = self.photo_url
		out["group"]     = self.group
		out["year"]      = self.year
		return out

	@staticmethod
	def encrypt(password):
		context = hashlib.md5()
		context.update(password)
		return context.hexdigest()

	@staticmethod
	def find(username, password):
		password_hash = User.encrypt(password)
		return User.query.filter_by(username = username, password_hash=password_hash).first()

	@staticmethod
	def verify_auth_token(token):
		s = TimedJSONWebSignatureSerializer(app.config["SECRET_KEY"])
		try:
			data = s.loads(token)
		except SignatureExpired:
			return None
		except BadSignature:
			return None
		user = User.query.get(data["id"])
		return user


# 论文表
class Paper(db.Model):
	id        = db.Column(db.Integer, primary_key=True)  # 论文ID
	title     = db.Column(db.String(1024))               # 标题
	authors   = db.Column(db.String(1024))               # 作者
	type      = db.Column(db.String(128))                # 类别: 会议/期刊
	publisher = db.Column(db.String(128))                # 会议名称或期刊名称
	year      = db.Column(db.Integer)                    # 发表年份
	pdf_url   = db.Column(db.String(1024))               # PDF文件URL

	def as_dict(self):
		out = {}
		out["id"]        = self.id
		out["title"]     = self.title
		out["authors"]   = self.authors
		out["type"]      = self.type
		out["publisher"] = self.publisher
		out["year"]      = self.year
		out["pdf_url"]   = self.pdf_url
		return out


# 绑定表
class Own(db.Model):
	id       = db.Column(db.Integer, primary_key=True)  # 拥有关系ID
	user_id  = db.Column(db.Integer)                    # 作者ID
	paper_id = db.Column(db.Integer)                    # 作者ID


