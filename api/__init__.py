import logging

import werkzeug.exceptions
from flask import Flask, request, jsonify

from api.user.requests import get_user_information
from database.mysql_connection import MySQL
from utils import constants

server = Flask(__name__)


@server.before_request
def log_request_info():
    pass


@server.after_request
def log_response_info(response):
    return response


@server.route("/dualis/user", methods=["GET", ])
def user_info():
    """
    Parse the user info. Required body json params are:

    username: "surname.lastname@domain",
    password: "password"

    :return: the parsed user information as json (for format see documentation)
    """
    code, result = get_user_information(request.get_json())

    if code == constants.BAD_LOGIN:
        # HTTP 401
        http_result = constants.HTTP_401_UNAUTHORIZED.copy()
        http_result["details"] = result
    elif code == constants.DUALIS_ERROR:
        # HTTP 503
        http_result = constants.HTTP_503_SERVICE_UNAVAILABLE.copy()
        http_result["details"] = "dualis request failed unexpectedly"
    elif code == constants.SUCCESS:
        # HTTP 200
        http_result = constants.HTTP_200_OK.copy()
        http_result["data"] = result

        mysql = MySQL()
        mysql.query(
            "INSERT INTO api_request VALUES(%s, CURRENT_TIMESTAMP(), 1) ON DUPLICATE KEY UPDATE last_update=CURRENT_TIMESTAMP(), request_count = request_count + 1",
            (result.get("username"),))
    else:
        # should never happen, internal server error
        http_result = constants.HTTP_500_INTERNAL_SERVER_ERROR.copy()
        http_result["details"] = "WTF? Impossible point of code reached"

    return jsonify(http_result), http_result["code"]


@server.errorhandler(Exception)
def exception_handler(error):
    """
    Return a error json string. If it is a werkzeug error (like 404 or 400) send a specific message, otherwise

    :param error: the exception that occurred
    :type error: Exception or werkzeug.exceptions.HTTPException

    :return: the json string and http status code for flask
    """

    # determine whether the exception is a HTTP exception
    if (issubclass(type(error), werkzeug.exceptions.HTTPException)):
        http_result = constants.HTTP_ERRORS.get(error.code, None)

        # if there is no template for this error create it
        if (http_result is None):
            http_result = {
                "code": error.code,
                "description": error.name
            }

        http_result["details"] = error.description
    else:
        # create an internal server error if a python exception occurred
        http_result = constants.HTTP_500_INTERNAL_SERVER_ERROR.copy()
        http_result["details"] = "Undefined Error. Please contact an administrator!"

        # log the exception stack trace
        logging.exception(type(error).__name__)

    return jsonify(http_result), http_result["code"]
