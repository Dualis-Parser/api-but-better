import api
from utils.logger import init_logger
from os import environ

if (__name__ == "__main__"):
    init_logger()

    server = api.server

    server.run(host='0.0.0.0', port=int(environ.get("PORT", 5000)))
