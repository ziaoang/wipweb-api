# encoding=utf-8

import sys
reload(sys)
sys.setdefaultencoding("utf8")


from db import g, app, db, auth, User, Paper, Own
from flask_restful import Api, Resource, reqparse
import random
import werkzeug
from datetime import datetime


api = Api(app)


def genUploadFileName():
	return "%s_%04d" % (datetime.now().strftime("%Y%m%d%H%M%S"), random.randint(0, 9999))


class LoginAPI(Resource):
	def post(self):
		parse = reqparse.RequestParser()
		parse.add_argument("username", type = str, required = True, help = "账号缺失")
		parse.add_argument("password", type = str, required = True, help = "密码缺失")
		args = parse.parse_args()
		user = User.find(args["username"], args["password"])
		if user == None:
			return {"status" : "error", "message" : "账号密码不匹配"}
		token = user.generate_auth_token()
		return { "status" : "ok", "id" : user.id , "token" : token }

api.add_resource(LoginAPI, '/api/login')


class UserAPI(Resource):
	def get(self):
		userList = []
		for user in User.query.all():
			userList.append(user.as_dict())
		return {"status" : "ok", "userList" : userList}

	@auth.login_required
	def post(self):
		parse = reqparse.RequestParser()
		parse.add_argument("username", type = str, required = True, help = "账号缺失")
		parse.add_argument("password", type = str, required = True, help = "密码缺失")
		args = parse.parse_args()
		user = User.query.filter_by(username = args["username"]).first()
		if user != None:
			return {"status" : "error", "message" : "用户已存在"}
		user = User()
		user.username      = args["username"]
		user.password_hash = User.encrypt(args["password"])
		db.session.add(user)
		db.session.commit()
		return {"status" : "ok", "message" : "用户创建成功"}


class UserIdAPI(Resource):
	def get(self, id):
		user = User.query.filter_by(id=id).first()
		if user == None: return {"status" : "error", "message" : "用户未找到"}
		return {"status" : "ok", "user" : user.as_dict()}

	@auth.login_required
	def put(self, id):
		user = User.query.filter_by(id=id).first()
		if user == None: return {"status" : "error", "message" : "用户未找到"}
		parse = reqparse.RequestParser()
		parse.add_argument("username",     type = str)
		parse.add_argument("old_password", type = str)
		parse.add_argument("new_password", type = str)
		parse.add_argument("alias",        type = str)
		parse.add_argument("cn_name",      type = str)
		parse.add_argument("en_name",      type = str)
		parse.add_argument("cn_intro",     type = str)
		parse.add_argument("en_intro",     type = str)
		parse.add_argument("photo",        type = werkzeug.datastructures.FileStorage, location='files')
		parse.add_argument("group",        type = str)
		parse.add_argument("year",         type = int)
		args = parse.parse_args()
		print args
		if args["username"] != None:
			user.username = args["username"]
		if args["old_password"] != None:
			if args["new_password"] != None:
				if user.password_hash == User.encrypt(args["old_password"]):
					user.password_hash = User.encrypt(args["new_password"])
				else:
					return {"status" : "error", "message" : "旧密码不匹配"}
			else:
				return {"status" : "error", "message" : "新密码未提供"}
		if args["alias"] != None:
			user.alias = args["alias"]
		if args["cn_name"] != None:
			user.cn_name = args["cn_name"]
		if args["en_name"] != None:
			user.en_name = args["en_name"]
		if args["cn_intro"] != None:
			user.cn_intro = args["cn_intro"]
		if args["en_intro"] != None:
			user.en_intro = args["en_intro"]
		if args["photo"] != None:
			audioFile = args["photo"]
			if audioFile.content_type == "image/jpeg":
				photo_url = app.config["UPLOAD_URL"] + genUploadFileName() + ".jpg"
				audioFile.save(app.config["PWD"] + photo_url)
				user.photo_url = photo_url
			elif audioFile.content_type == "image/png":
				photo_url = app.config["UPLOAD_URL"] + genUploadFileName() + ".png"
				audioFile.save(app.config["PWD"] + photo_url)
				user.photo_url = photo_url
			else:
				return {"status" : "error", "message" : "头像格式仅支持JPG和PNG"}
		if args["group"] != None:
			user.group = args["group"]
		if args["year"] != None:
			user.year = args["year"]
		db.session.commit()
		return {"status" : "ok", "message" : "用户更新成功"}

	@auth.login_required
	def delete(self, id):
		user = User.query.filter_by(id=id).first()
		if user == None: return {"status" : "error", "message" : "用户未找到"}
		db.session.delete(user)
		db.session.commit()
		return {"status" : "ok", "message" : "用户删除成功"}


class UserGroupAPI(Resource):
	def get(self, group):
		userList = []
		for user in User.query.filter_by(group=group).all():
			userList.append(user.as_dict())
		return {"status" : "ok", "userList" : userList}


api.add_resource(UserAPI, '/api/user')
api.add_resource(UserIdAPI, '/api/user/id/<int:id>')
api.add_resource(UserGroupAPI, '/api/user/group/<string:group>')


class PaperAPI(Resource):
	def get(self):
		paperList = []
		for paper in Paper.query.all():
			paperList.append(paper.as_dict())
		return {"status" : "ok", "paperList" : paperList}

	@auth.login_required
	def post(self):
		parse = reqparse.RequestParser()
		parse.add_argument("title",     type = str, required = True, help = "论文标题缺失")
		parse.add_argument("authors",   type = str, required = True, help = "论文作者缺失")
		parse.add_argument("type",      type = str, required = True, help = "论文类别缺失")
		parse.add_argument("publisher", type = str, required = True, help = "会议名称/期刊名称缺失")
		parse.add_argument("year",      type = int, required = True, help = "发表年份缺失")
		parse.add_argument("pdf",       type = werkzeug.datastructures.FileStorage, location='files', required = True, help = "PDF文件缺失")
		args = parse.parse_args()
		paper = Paper()
		paper.title     = args["title"];
		paper.authors   = args["authors"];
		paper.type      = args["type"];
		paper.publisher = args["publisher"];
		paper.year      = args["year"];
		audioFile = args["pdf"]
		if audioFile.content_type == "application/pdf":
			pdf_url = app.config["UPLOAD_URL"] + genUploadFileName() + ".pdf"
			audioFile.save(app.config["PWD"] + pdf_url)
			paper.pdf_url = pdf_url
		else:
			return {"status" : "error", "message" : "论文文件只支持PDF格式"}
		db.session.add(paper)
		db.session.commit()
		own = Own()
		own.user_id  = g.user.id
		own.paper_id = paper.id
		db.session.add(own)
		db.session.commit()
		return {"status" : "ok", "paper" : "论文创建成功"}


class PaperIdAPI(Resource):
	def get(self, id):
		paper = Paper.query.filter_by(id=id).first()
		if paper == None: return {"status" : "error", "message" : "论文未找到"}
		return {"status" : "ok", "paper" : paper.as_dict()}

	@auth.login_required
	def put(self, id):
		paper = Paper.query.filter_by(id=id).first()
		if paper == None: return {"status" : "error", "message" : "论文未找到"}
		parse = reqparse.RequestParser()
		parse.add_argument("title",     type = str)
		parse.add_argument("authors",   type = str)
		parse.add_argument("type",      type = str)
		parse.add_argument("publisher", type = str)
		parse.add_argument("year",      type = int)
		parse.add_argument("pdf",       type = werkzeug.datastructures.FileStorage, location='files')
		args = parse.parse_args()
		print args
		if args["title"] != None:
			paper.title = args["title"]
		if args["authors"] != None:
			paper.authors = args["authors"]
		if args["type"] != None:
			paper.type = args["type"]
		if args["publisher"] != None:
			paper.publisher = args["publisher"]
		if args["year"] != None:
			paper.year = args["year"]
		if args["pdf"] != None:
			audioFile = args["pdf"]
			if audioFile.content_type == "application/pdf":
				pdf_url = app.config["UPLOAD_URL"] + genUploadFileName() + ".pdf"
				audioFile.save(app.config["PWD"] + pdf_url)
				paper.pdf_url = pdf_url
			else:
				return {"status" : "error", "message" : "论文文件只支持PDF格式"}
		db.session.commit()
		return {"status" : "ok", "message" : "论文更新成功"}

	@auth.login_required
	def delete(self, id):
		paper = Paper.query.filter_by(id=id).first()
		if paper == None: return {"status" : "error", "message" : "论文未找到"}
		db.session.delete(paper)
		db.session.commit()
		return {"status" : "ok", "message" : "论文删除成功"}


class PaperUserIdAPI(Resource):
	def get(self, id):
		paperList = []
		for own in Own.query.filter_by(user_id=id).all():
			paper = Paper.query.filter_by(id=own.paper_id).first()
			paperList.append(paper.as_dict())
		return {"status" : "ok", "paperList" : paperList}


class PaperKeywordAPI(Resource):
	@auth.login_required
	def post(self):
		parse = reqparse.RequestParser()
		parse.add_argument("keyword", type = str, required = True, help = "关键词缺失")
		args = parse.parse_args()
		keyword = args["keyword"]
		selfPaperIdSet = set()
		for own in Own.query.filter_by(user_id=g.user.id).all():
			selfPaperIdSet.add(own.paper_id)
		paperList = []
		for paper in Paper.query.filter(Paper.title.contains(keyword) | Paper.authors.contains(keyword) | Paper.publisher.contains(keyword)).all():
			item = paper.as_dict()
			if paper.id in selfPaperIdSet:
				item["is_own"] = True
			else:
				item["is_own"] = False
			paperList.append(item)
		return {"status" : "ok", "paperList" : paperList}


api.add_resource(PaperAPI, '/api/paper')
api.add_resource(PaperIdAPI, '/api/paper/id/<int:id>')
api.add_resource(PaperUserIdAPI, '/api/paper/user_id/<int:id>')
api.add_resource(PaperKeywordAPI, '/api/paper/keyword')


class OwnAPI(Resource):
	@auth.login_required
	def post(self):
		parse = reqparse.RequestParser()
		parse.add_argument("paper_id", type = int, required = True, help = "论文ID缺失")
		args = parse.parse_args()
		print args["paper_id"]
		own = Own.query.filter_by(user_id=g.user.id, paper_id=args["paper_id"]).first()
		if own != None:
			return {"status" : "error", "message" : "绑定关系已存在"}
		own = Own()
		own.user_id  = g.user.id
		own.paper_id = args["paper_id"]
		db.session.add(own)
		db.session.commit()
		return {"status" : "ok", "message" : "绑定添加成功"}

	@auth.login_required
	def delete(self):
		parse = reqparse.RequestParser()
		parse.add_argument("paper_id", type = int, required = True, help = "论文ID缺失")
		args = parse.parse_args()
		print args["paper_id"]
		own = Own.query.filter_by(user_id=g.user.id, paper_id=args["paper_id"]).first()
		if own == None:
			return {"status" : "error", "message" : "绑定关系不存在"}
		db.session.delete(own)
		db.session.commit()
		return {"status" : "ok", "message" : "绑定解除成功"}


api.add_resource(OwnAPI, '/api/own')


if __name__ == '__main__':
	app.run()


