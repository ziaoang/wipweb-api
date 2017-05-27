# encoding=utf-8

import sys
reload(sys)
sys.setdefaultencoding("utf8")


from db import db, as_dict, User, Paper, News
from datetime import datetime


def init_user():
	userList = []
	for line in open('data/user.txt'):
		t = line.strip().split('\t')
		user = User()
		user.chinese_name    = t[1]
		user.photo_url       = t[2]
		user.alias           = t[3]
		user.enrollment_year = int(t[4])
		user.group           = t[5]
		user.introduction    = t[6]
		userList.append(user)
	db.session.add_all(userList)
	db.session.commit()


def init_paper():
	paperList = []
	for line in open('data/paper.txt'):
		t = line.strip().split('\t')
		paper = Paper()
		paper.title          = t[0]
		paper.publish_year   = int(t[1])
		paper.publisher_name = t[2]
		paper.publisher_url  = t[3]
		paper.publish_type   = t[4]
		paper.pdf_url        = t[5]
		paperList.append(paper)
	db.session.add_all(paperList)
	db.session.commit()


def init_news():
	newsList = []
	for line in open('data/news.txt'):
		t = line.strip().split('\t')
		news = News()
		news.title       = t[0]
		news.content     = t[1]
		news.create_time = datetime.now()
		news.update_time = datetime.now()
		newsList.append(news)
	db.session.add_all(newsList)
	db.session.commit()


def main():
	init_user()
	init_paper()
	init_news()


if __name__ == '__main__':
	main()


