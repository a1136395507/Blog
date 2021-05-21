import logging, json
from .. import bp
from flask import request, render_template, jsonify

logger = logging.getLogger(__name__)


@bp.route("/index", methods=["GET"])
def hello_demo():
    logger.info("just a test!")
    ret = {"status": 1, "message": "ok", "data": None}
    return jsonify(json.loads(json.dumps(ret)))


@bp.route("/login", methods=["GET", "POST"])
def login_():
    if request.method == "GET":
        return render_template("login.html")
    else:
        username = request.get("username")
        password = request.get("password")
        print(username)
        print(password)

        ret = {"status": 1, "message": "ok", "data": {"username": username}, "password": password}
        return jsonify(json.loads(json.dumps(ret)))


@bp.route("/register", method=["GET", "POST"])
def register_():
    if request.method == "GET":
        pass
    else:
        pass


# internale msg dog eC  buy

# 
