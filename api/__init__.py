import json
import logging

import werkzeug.exceptions
from flask import Flask, request, jsonify
from flask_cors import CORS

from api.user.requests import get_user_information, is_authenticated_user
from utils import constants

server = Flask(__name__)
CORS(server)


@server.before_request
def log_request_info():
    pass


@server.after_request
def log_response_info(response):
    return response


@server.route("/user/<string:username>", methods=["GET", ])
def user_info(username: str):
    """
    Parse the user info.

    username: "surname.lastname@domain" - as url content
    password: "password" - as Private-Token header

    :param username: The username

    :return: the parsed user information as json (for format see documentation)
    """
    code, result = get_user_information({"username": username, "password": request.headers.get("Private-Token")})

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

        user = result.get("username")

        from database.mysql_connection import MySQL
        mysql = MySQL()
        mysql.query("INSERT INTO api_request VALUES(%s, CURRENT_TIMESTAMP(), 1) ON DUPLICATE KEY UPDATE "
                    "last_update=CURRENT_TIMESTAMP(), request_count = request_count + 1", (user,))
        for module in result.get("modules"):
            module_no = module.get("module_no")
            grade = module.get("final_grade")
            passed = module.get("passed")
            exams = json.dumps(module.get("grades"))

            grade = grade if grade.replace('.', '', 1).isdigit() else None

            mysql.query(
                "INSERT INTO new_module VALUES(%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE "
                "grade=%s, passed=%s, exams=%s",
                (user, module_no, grade, passed, exams, grade, passed, exams)
            )
        mysql.close()

    else:
        # should never happen, internal server error
        http_result = constants.HTTP_500_INTERNAL_SERVER_ERROR.copy()
        http_result["details"] = "WTF? Impossible point of code reached"

    return jsonify(http_result), http_result["code"]


@server.route("/user/validate/<string:username>", methods=["GET", ])
def is_valid_user(username: str):
    """
    Return whether the given user data is valid

    :return: true or false
    :rtype: bool
    """
    result = is_authenticated_user({"username": username, "password": request.headers.get("Private-Token")})
    if (result == constants.DUALIS_ERROR):
        # dualis error
        http_result = constants.HTTP_503_SERVICE_UNAVAILABLE.copy()
        http_result["details"] = "dualis request failed unexpectedly"
    elif result == constants.BAD_REQUEST:
        # malformed request
        http_result = constants.HTTP_400_BAD_REQUEST.copy()
        http_result["details"] = "the server couldn't understand your request"
    elif result is False or result is True:
        # send bool response
        http_result = constants.HTTP_200_OK.copy()
        http_result["data"] = result
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
