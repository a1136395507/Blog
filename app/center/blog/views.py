from . import bp
from run import app
from flask import request
from flask import render_template, url_for
from traceback import format_exc
logging = app.logger


# 测试页面
@bp.route("/index", methods=["GET", "POST"])
def home_test():
    if request.method == "GET":
        return {"status": "success", "data": [], "message": "测试成功"}


@bp.route("/", methods=["GET"])
def index_html():
    try:

        return render_template("index.html")
    except:
        print(format_exc())
        return "出错了"
