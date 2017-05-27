# encoding=utf-8

import sys
reload(sys)
sys.setdefaultencoding("utf8")


from api import app


if __name__ == '__main__':
	app.run()


