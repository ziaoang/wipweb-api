# encoding=utf-8

import sys
reload(sys)
sys.setdefaultencoding("utf8")

from flask import Flask, make_response, jsonify


app = Flask(__name__)


@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({"status" : "error", "message" : "404"}), 404)


