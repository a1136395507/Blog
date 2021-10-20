from . import bp
from run import app
from flask import request

logging = app.logger


# 测试页面
@bp.route("/", methods=["GET", "POST"])
def home_test():
    if request.method == "GET":

        return {"status": "success", "data": [], "message": "测试成功"}
