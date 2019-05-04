from utils import constants
from utils.constants import POST_FIELDS, DUALIS_BASE_URI, MAIN_SCRIPT
from utils.make_http_request import make_request


def do_login(session, username, password):
    """
    Perform the dualis login with redirects (resulting page will be home)

    :param session: the session to log into
    :param username: the username
    :param password: the password

    :type session: requests.Session
    :type username: str
    :type password: str

    :return: the home page response or an error code
    :rtype: requests.Response or int
    """
    # get the necessary post fields cuz dualis wants to
    login_data = POST_FIELDS.copy()
    login_data["usrname"] = username
    login_data["pass"] = password

    response = make_request(session, DUALIS_BASE_URI + MAIN_SCRIPT, login_data, "POST", True)

    # check if the login was successful
    if "Benutzername oder Passwort falsch" in response.text:
        return constants.BAD_LOGIN
    return response
