import requests

from dualis import login
from dualis.user import parse_users_name, parse_users_modules
from dualis.util import *
from utils import constants
from utils.mail import is_valid_email
from utils.make_http_request import make_request


def get_user_information(request):
    """
    Get the user information (for format check the docs)

    :param request: the request json body
    :type request: dict
    :return: the user information
    """
    # validate login credentials (format only)

    if type(request) != dict:
        return constants.BAD_LOGIN, "Invalid content sent"
    elif "username" not in request.keys() or "password" not in request.keys():
        return constants.BAD_LOGIN, "Invalid content sent"

    elif not is_valid_email(request.get("username")):
        return constants.BAD_LOGIN, "Invalid username format"

    user_info = parse_user_information(request.get("username"), request.get("password"))
    if user_info == constants.BAD_LOGIN:
        return constants.BAD_LOGIN, "Invalid username or password"
    elif user_info == constants.DUALIS_ERROR:
        return constants.DUALIS_ERROR, None

    return constants.SUCCESS, user_info


def parse_user_information(username, password):
    """
    All relevant parsing calls for the user information api call happens in here

    :param username: the dualis username (valid email format)
    :param password: the dualis password (plain)

    :type username: str
    :type password: str

    :return: the complete user information
    """

    # build the return data template
    user_data = constants.USER_DATA.copy()
    user_data["username"] = username

    # start a session to save the cookies
    with requests.Session() as session:
        # perform the login
        login_res = login.do_login(session, username, password)

        if (not isinstance(login_res, requests.Response)):
            if login_res == constants.BAD_LOGIN:
                return constants.BAD_LOGIN
            else:
                return constants.DUALIS_ERROR

        # find the users name in the html
        user_data["name"] = parse_users_name(login_res.text)

        # find the navigation list
        user_data["navigation"] = dict(get_navigation(login_res.text))

        # find the exams page (for all languages)
        exams_page_url = constants.DUALIS_BASE_URI
        for link in user_data["navigation"].values():
            if (constants.EXAM_OVERVIEW_PAGE in link):
                exams_page_url += link

        # navigate to the exams page
        exams_page = make_request(session, exams_page_url, None, "get", False)

        # get all semester names and url parameters
        semesters = dict(parse_semesters(exams_page.text))
        user_data["semesters"] = list(semesters.keys())

        # remove first semester from the list, we got that html already
        curr_semester_name = list(semesters.keys())[0]
        semesters.pop(curr_semester_name)

        # get the html for all semesters
        semester_html = {curr_semester_name: exams_page.text}

        for name, url_param in semesters.items():
            semester = make_request(session, exams_page_url + url_param, method="get")
            semester_html[name] = semester.text

        # get all modules for all semesters
        user_data["modules"] = parse_users_modules(semester_html)

    return user_data
