# internal error codes
SUCCESS: int = 0
BAD_LOGIN: int = 1
DUALIS_ERROR: int = 2
BAD_REQUEST: int = 3

# HTTP responses
HTTP_200_OK = {
    "code": 200,
    "description": "OK"
}

HTTP_400_BAD_REQUEST = {
    "code": 400,
    "description": "Bad Request"
}

HTTP_401_UNAUTHORIZED = {
    "code": 401,
    "description": "Unauthorized"
}

HTTP_404_NOT_FOUND = {
    "code": 404,
    "description": "Not Found"
}

HTTP_500_INTERNAL_SERVER_ERROR = {
    "code": 500,
    "description": "Internal Server Error"
}

HTTP_503_SERVICE_UNAVAILABLE = {
    "code": 503,
    "description": "Service Unavailable"
}

HTTP_ERRORS = {
    200: HTTP_200_OK,
    400: HTTP_400_BAD_REQUEST,
    401: HTTP_401_UNAUTHORIZED,
    404: HTTP_404_NOT_FOUND,
    500: HTTP_500_INTERNAL_SERVER_ERROR,
    503: HTTP_503_SERVICE_UNAVAILABLE
}

# dualis constants

# idk what the most shit is used form, but without the request fucks up
POST_FIELDS = {
    'APPNAME': 'CampusNet',  # this is just always CampusNet, maybe you figure out why?
    'PRGNAME': 'LOGINCHECK',  # this actually makes some sense, it's the page you are requesting
    'ARGUMENTS': 'clino,usrname,pass,menuno,menu_type,browser,platform',  # holy fuck is this???
    'clino': '000000000000001',  # obviously the language you wanna use, doesn't really matter in our case, I guess
    'menuno': '000000',  # yes
    'menu_type': 'classic',  # also yes
    'browser': '',  # just always empty
    'platform': '',  # same
    'usrname': '',  # the username, but the additional e would be too long, so they just removed it
    'pass': ''  # the password... obviously
}

DUALIS_BASE_URI = "https://dualis.dhbw.de"

# u can recognize a good site based on the fact, that all fucking contents are received from a fucking dll
MAIN_SCRIPT = "/scripts/mgrqispi.dll"

EXAM_OVERVIEW_PAGE = "COURSERESULTS"

MODULE_DATA = {
    'module_no': '',
    'module_name': '',
    'final_grade': '',
    'credits': '',
    'exams_url': '',
    'passed': False,
    'grades': [],
    'semesters': ''
}

USER_DATA = {
    'username': '',
    'name': '',
    'navigation': {},
    'modules': [],
    'semesters': []
}

EXAM_DATA = {
    'name': '',
    'grade': None,
}

GRADE_FILTERS = ["not set yet", "noch nicht gesetzt"]