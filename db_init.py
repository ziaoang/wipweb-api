# encoding=utf-8

import sys
reload(sys)
sys.setdefaultencoding("utf8")


from db import db, User


def init_user():	
	admin_username = "admin"
	admin_password = "icstwip"
	user = User()
	user.username      = admin_username
	user.password_hash = User.encrypt(admin_password)
	db.session.add(user)
	db.session.commit()


if __name__ == "__main__":
	init_user()


