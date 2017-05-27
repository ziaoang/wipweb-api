# encoding=utf-8

import sys
reload(sys)
sys.setdefaultencoding("utf8")

from app import app
from db import db, as_dict, User, Paper, News
from flask_restful import Api, Resource, reqparse
from datetime import datetime


api = Api(app)


user_parse = reqparse.RequestParser()
user_parse.add_argument('username',        type = str, required = True, help = 'username needed',        location = 'json')
user_parse.add_argument('password_hash',   type = str, required = True, help = 'password_hash needed',   location = 'json')
user_parse.add_argument('chinese_name',    type = str, required = True, help = 'chinese_name needed',    location = 'json')
user_parse.add_argument('name_in_paper',   type = str, required = True, help = 'name_in_paper needed',   location = 'json')
user_parse.add_argument('alias',           type = str, required = True, help = 'alias needed',           location = 'json')
user_parse.add_argument('gender',          type = str, required = True, help = 'gender needed',          location = 'json')
user_parse.add_argument('group',           type = str, required = True, help = 'group needed',           location = 'json')
user_parse.add_argument('photo_url',       type = str, required = True, help = 'photo_url needed',       location = 'json')
user_parse.add_argument('enrollment_year', type = int, required = True, help = 'enrollment_year needed', location = 'json')
user_parse.add_argument('graduation_year', type = int, required = True, help = 'graduation_year needed', location = 'json')
user_parse.add_argument('introduction',    type = str, required = True, help = 'introduction needed',    location = 'json')


class UserAPI(Resource):
	def get(self):
		userList = []
		for user in User.query.all():
			userList.append(as_dict(user))
		return {"status" : "ok", "userList" : userList}

	def post(self):
		args = user_parse.parse_args()
		user = User(args)
		db.session.add(user)
		db.session.commit()
		return {"status" : "ok", "user" : as_dict(user)}


class UserIdAPI(Resource):
	def get(self, id):
		user = User.query.filter_by(id=id).first()
		if user == None: return {"status" : "error", "message" : "user id not found"}
		return {"status" : "ok", "user" : as_dict(user)}

	def put(self, id):
		user = User.query.filter_by(id=id).first()
		if user == None: return {"status" : "error", "message" : "user id not found"}
		args = user_parse.parse_args()
		user.update(args)
		db.session.commit()
		return {"status" : "ok", "user" : as_dict(user)}

	def delete(self, id):
		user = User.query.filter_by(id=id).first()
		if user == None: return {"status" : "error", "message" : "user id not found"}
		db.session.delete(user)
		db.session.commit()
		return {"status" : "ok", "message" : "delete successfully"}


class UserGroupAPI(Resource):
	def get(self, group):
		userList = []
		for user in User.query.filter_by(group=group).all():
			userList.append(as_dict(user))
		return {"status" : "ok", "userList" : userList}


api.add_resource(UserAPI, '/api/user')
api.add_resource(UserIdAPI, '/api/user/id/<int:id>')
api.add_resource(UserGroupAPI, '/api/user/group/<string:group>')


paper_parse = reqparse.RequestParser()
paper_parse.add_argument('title',          type = str, required = True, help = 'title needed',          location = 'json')
paper_parse.add_argument('authors',        type = str, required = True, help = 'authors needed',        location = 'json')
paper_parse.add_argument('publisher_name', type = str, required = True, help = 'publisher_name needed', location = 'json')
paper_parse.add_argument('publisher_url',  type = str, required = True, help = 'publisher_url needed',  location = 'json')
paper_parse.add_argument('publish_type',   type = str, required = True, help = 'publish_type needed',   location = 'json')
paper_parse.add_argument('publish_year',   type = int, required = True, help = 'publish_year needed',   location = 'json')
paper_parse.add_argument('pdf_url',        type = str, required = True, help = 'pdf_url needed',        location = 'json')


class PaperAPI(Resource):
	def get(self):
		paperList = []
		for paper in Paper.query.all():
			paperList.append(as_dict(paper))
		return {"status" : "ok", "paperList" : paperList}

	def post(self):
		args = paper_parse.parse_args()
		paper = Paper(args)
		db.session.add(paper)
		db.session.commit()
		return {"status" : "ok", "paper" : as_dict(paper)}


class PaperIdAPI(Resource):
	def get(self, id):
		paper = Paper.query.filter_by(id=id).first()
		if paper == None: return {"status" : "error", "message" : "paper id not found"}
		return {"status" : "ok", "paper" : as_dict(paper)}

	def put(self, id):
		paper = Paper.query.filter_by(id=id).first()
		if paper == None: return {"status" : "error", "message" : "paper id not found"}
		args = paper_parse.parse_args()
		paper.update(args)
		db.session.commit()
		return {"status" : "ok", "paper" : as_dict(user)}

	def delete(self, id):
		paper = Paper.query.filter_by(id=id).first()
		if paper == None: return {"status" : "error", "message" : "paper id not found"}
		db.session.delete(paper)
		db.session.commit()
		return {"status" : "ok", "message" : "delete successfully"}


api.add_resource(PaperAPI, '/api/paper')
api.add_resource(PaperIdAPI, '/api/paper/id/<int:id>')


news_parse = reqparse.RequestParser()
news_parse.add_argument('title',   type = str, required = True, help = 'title needed',   location = 'json')
news_parse.add_argument('content', type = str, required = True, help = 'content needed', location = 'json')


class NewsAPI(Resource):
	def get(self):
		newsList = []
		for news in News.query.all():
			newsList.append(as_dict(news))
		return {"status" : "ok", "newsList" : newsList}

	def post(self):
		args = news_parse.parse_args()
		news = News(args)
		db.session.add(news)
		db.session.commit()
		return {"status" : "ok", "news" : as_dict(news)}


class NewsIdAPI(Resource):
	def get(self, id):
		news = News.query.filter_by(id=id).first()
		if news == None: return {"status" : "error", "message" : "new id not found"}
		return {"status" : "ok", "news" : as_dict(news)}

	def put(self, id):
		news = News.query.filter_by(id=id).first()
		if news == None: return {"status" : "error", "message" : "new id not found"}
		args = news_parse.parse_args()
		news.update(args)
		db.session.commit()
		return {"status" : "ok", "news" : as_dict(news)}

	def delete(self, id):
		news = News.query.filter_by(id=id).first()
		if news == None: return {"status" : "error", "message" : "new id not found"}
		db.session.delete(news)
		db.session.commit()
		return {"status" : "ok", "message" : "delete successfully"}


class NewsPageAPI(Resource):
	def get(self, start, count):
		newsList = []
		for news in News.query.order_by(News.datetime).offset(start).limit(count):
			newss.append(as_dict(news))
		return {"status" : "ok", "newsList" : newsList}


api.add_resource(NewsAPI, '/api/news')
api.add_resource(NewsIdAPI, '/api/news/id/<int:id>')
api.add_resource(NewsPageAPI, '/api/news/start/<int:start>/count/<int:count>')


