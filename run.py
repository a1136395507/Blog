import os
import logging
import traceback
from app import create_app, db
from flask import jsonify, request, redirect, url_for
from sqlalchemy.exc import DatabaseError
from flask_script import Manager
from flask_migrate import Migrate

app = create_app(os.getenv('APP_RUN_ENV') or 'dev')
logger = app.logger
if app.config.get("DEBUG"):
    logger.setLevel(logging.DEBUG)


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


@app.errorhandler(Exception)
def error_500(error):
    if isinstance(error, DatabaseError):
        msg = str(error._message())
    else:
        msg = str(error)
    ret = dict(status=500, message=msg, data=None)
    logger.error(traceback.format_exc())
    return jsonify(ret), 200


@app.after_request
def post_response(response):
    logger.debug("this is {} responding".format(os.getpid()))
    return response


manager = Manager(app)
migrate = Migrate(app, db)

if __name__ == '__main__':
    manager.run()
