import json
import logging

import werkzeug.exceptions
from flask import Flask, request, jsonify, session, copy_current_request_context
from flask_socketio import SocketIO, emit, disconnect
from flask_cors import CORS
from healthcheck import HealthCheck

from api.user.requests import get_user_information, is_authenticated_user
from utils import constants
from utils.http_object_prepare import prepare_from_user_auth, prepare_from_user_info

async_mode = None

server = Flask(__name__)
socket_ = SocketIO(server, async_mode=async_mode, cors_allowed_origins='*')
CORS(server)

health = HealthCheck()


def dualis_available():
    return constants.DUALIS_OK, "dualis web " + "ok" if constants.DUALIS_OK else "down"


health.add_check(dualis_available)
server.add_url_rule("/healthcheck", "healthcheck", view_func=lambda: health.run())


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

    http_result = prepare_from_user_info(code, result)

    return jsonify(http_result), http_result["code"]


@server.route("/user/validate/<string:username>", methods=["GET", ])
def is_valid_user(username: str):
    """
    Return whether the given user data is valid

    :return: true or false
    """
    result = is_authenticated_user({"username": username, "password": request.headers.get("Private-Token")})
    http_result = prepare_from_user_auth(result)

    return jsonify(http_result), http_result["code"]


@socket_.on('user_auth')
def ws_is_valid_user(message):
    logging.info("Received user_auth message")
    session["username"] = message.get("username", None)
    session["password"] = message.get("password", None)

    result = is_authenticated_user({"username": session.get("username"), "password": session.get("password")})
    http_result = prepare_from_user_auth(result)

    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('user_auth_response', http_result)


@socket_.on('user_info')
def ws_user_info():
    if not (session.get("username") or session.get("password")):
        http_result = constants.HTTP_401_UNAUTHORIZED.copy()
        http_result["details"] = "Authorization required! (call user_auth)"
        emit('user_info_response', http_result)

    logging.info("Request for module data by {}".format(session.get("username")))
    code, result = get_user_information({"username": session.get("username"), "password": session.get("password")}, emit)

    if code == constants.BAD_LOGIN or code == constants.DUALIS_ERROR:
        http_result = constants.HTTP_503_SERVICE_UNAVAILABLE.copy()
        http_result["details"] = "dualis request failed unexpectedly"
    else:
        http_result = constants.HTTP_204_NO_CONTENT.copy()
        http_result["details"] = "all contents loaded"
    emit('user_info_response', http_result)


@socket_.on('disconnect_request')
def disconnect_request():
    @copy_current_request_context
    def can_disconnect():
        disconnect()

    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'Disconnected!', 'count': session['receive_count']},
         callback=can_disconnect)


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
