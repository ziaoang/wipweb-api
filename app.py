# encoding=utf-8

import sys
reload(sys)
sys.setdefaultencoding("utf8")

from flask import Flask, make_response, jsonify


app = Flask(__name__)


@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({"status" : "error", "message" : "404"}), 404)


@app.after_request
def after_request(response):
	response.headers.add('Access-Control-Allow-Origin', '*')
	response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
	response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
	return response


