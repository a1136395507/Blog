import os, traceback
from app import create_app
from flask import jsonify, request
# from sqlalchemy.exc import DatabaseError
from flask_script import Manager


app = create_app("prd")

logger = app.logger


@app.before_request
def log_request_info():
    _msg = "[审计日志]: [%s][%s],[%s],[%s]" % (request.method, request.path, str(request.args.to_dict()), str(request.json))


@app.errorhandler(ArithmeticError)
def handle_invalid_usage(error):
    ret = error.to_dict()
    logger.error(traceback.format_exc(ret))
    return jsonify(ret)


@app.errorhandler(404)
def error_404(error):
    ret = dict(status=404, message="404 not Found", data=None)
    return jsonify(ret), 404


# @app.errorhandler(Exception)
# def error_500(error):
#     if isinstance(error, DatabaseError):
#         msg = str(error._message())
#     else:
#         msg = str(error)
#     ret = dict(status=500, message=msg, data=None)
#     logger.error(traceback.format_exc())
#     return jsonify(ret), 200

@app.after_request
def post_response(response):
    logger.debug("this is {} responding".format(os.getpid()))
    return response

# @app.route("/index",methods=['GET'])
# def index():
#
#     return render_template("/index.html")
manager = Manager(app)


if __name__ == '__main__':
    manager.run()
