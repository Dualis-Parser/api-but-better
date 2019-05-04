from bs4 import BeautifulSoup

from utils import constants


def parse_refresh(value):
    """
    Parse the url from a refresh tag or header
    :param value: the content of the tag or header
    :type value: str

    :return: the url
    :rtype: str
    """
    return "=".join(value.split("=")[1::])


def do_follow_redirects(session, response):
    """
    Search the response for any redirect (header or html head) and follow them

    :param session: the current session
    :param response: the response to search

    :type session: requests.Session
    :type response: requests.Response

    :return: the new response
    :rtype: requests.Response
    """
    redirect_target = False
    if "REFRESH" in response.headers.keys():
        # get the url path
        redirect_target = parse_refresh(response.headers["REFRESH"])
    else:
        # search for possible meta refresh tag
        soup = BeautifulSoup(response.text, 'lxml')
        refresh = soup.find("meta", {"http-equiv": "refresh"})
        if refresh:
            redirect_target = parse_refresh(refresh.get("content"))[:-1]

    if (redirect_target):
        return make_request(session, constants.DUALIS_BASE_URI + redirect_target, None, "GET", True)
    else:
        return response


def make_request(session, url, data=None, method="POST", follow_redirects=True):
    """
    Make a get request to a specific url with parameters

    :param session: the requests session
    :param url: the target url
    :param data: the parameters
    :param method: the request method
    :param follow_redirects: whether to follow redirects in headers or html meta tag

    :type session: requests.Session
    :type url: str
    :type data: dict or None
    :type method: str
    :type follow_redirects: bool

    :return: the response
    :rtype: requests.Response
    """
    if (method.lower() == "get"):
        response = session.get(url, data=data, allow_redirects=follow_redirects)
    elif (method.lower() == "post"):
        response = session.post(url, data=data, allow_redirects=follow_redirects)
    elif (method.lower() == "delete"):
        response = session.delete(url, data=data, allow_redirects=follow_redirects)
    elif (method.lower() == "put"):
        response = session.put(url, data=data, allow_redirects=follow_redirects)
    elif (method.lower() == "head"):
        response = session.head(url, data=data, allow_redirects=follow_redirects)
    elif (method.lower() == "options"):
        response = session.options(url, data=data, allow_redirects=follow_redirects)
    elif (method.lower() == "patch"):
        response = session.patch(url, data=data, allow_redirects=follow_redirects)
    else:
        raise ValueError("Unknown request method %s" % method)

    response.encoding = "UTF-8"

    return do_follow_redirects(session, response) if follow_redirects else response
