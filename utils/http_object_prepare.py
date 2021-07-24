from utils import constants


def prepare_from_user_auth(result):
    http_result = None
    if result == constants.DUALIS_ERROR:
        constants.DUALIS_OK = False
        # dualis error
        http_result = constants.HTTP_503_SERVICE_UNAVAILABLE.copy()
        http_result["details"] = "dualis request failed unexpectedly"
    elif result == constants.BAD_REQUEST:
        # malformed request
        http_result = constants.HTTP_400_BAD_REQUEST.copy()
        http_result["details"] = "the server couldn't understand your request"
    elif result is False or result is True:
        constants.DUALIS_OK = True
        # send bool response
        http_result = constants.HTTP_200_OK.copy()
        http_result["data"] = result
    else:
        # should never happen, internal server error
        http_result = constants.HTTP_500_INTERNAL_SERVER_ERROR.copy()
        http_result["details"] = "WTF? Impossible point of code reached. Congrats"
    return http_result
