import api
from utils.logging import init_logger

if (__name__ == "__main__"):
    init_logger()

    server = api.server

    server.run(port=8081)
