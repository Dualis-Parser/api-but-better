import api
from utils.logger import init_logger

if (__name__ == "__main__"):
    init_logger()

    server = api.server

    server.run(host='0.0.0.0')
