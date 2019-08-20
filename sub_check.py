from multiprocessing.pool import ThreadPool as Pool

import requests

from database.mysql_connection import MySQL
from cryptography.fernet import Fernet
from base64 import b64decode

from secret_config import app_secret
from utils.mail import send_html_mail


def dec(message, password=app_secret):
    cipher = b64decode(message)
    cipher_suite = Fernet(password)
    cipher_text = cipher_suite.decrypt(cipher)
    return cipher_text


def check_and_send_mail(user):
    username = user[0]
    password = dec(user[1])

    r = requests.get(url="http://localhost:9001/dualis/user", params={'username': username, 'password': password})
    user_info = r.json()
    if (user_info["code"] == 401):
        mysql.query("UPDATE `subscription` SET `valid` = FALSE WHERE `username` = ?", [username, ])
    elif (user_info["code"] != 200):
        return
    else:
        message = ""
        send = False
        for module in user_info["data"]["modules"]:
            if (module["updated"]):
                send = True
                message += "<p><b>{}: {}</b></p>".format(module["module_name"], module["final_grade"])
                message += "<table style='margin-left: 5em'>"
                for grade in module["grades"]:
                    message += "<tr>"
                    message += "<td>{}:</td><td>{}</td>".format(grade["name"], grade["grade"])
                    message += "</tr>"
                message += "</table>"
        if (send):
            send_html_mail(user_info["data"]["name"], user[2], "Dualis Parser - Grades Updated!", message)


if __name__ == '__main__':
    mysql = MySQL()
    to_check = mysql.query("SELECT * FROM `subscription` WHERE `valid`", [])

    pool = Pool(8)
    for user in to_check:
        pool.apply_async(check_and_send_mail, (user,))

    pool.close()
    pool.join()
