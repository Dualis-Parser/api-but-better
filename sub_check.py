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


def check_and_send_mail(user) -> bool:
    username = user[1]
    password = dec(user[2])

    print("Checking for " + username)

    r = requests.get(url="http://localhost:9001/dualis/user", params={'username': username, 'password': password})
    user_info = r.json()
    if (user_info["code"] == 401):
        mysql.query("UPDATE `course` SET `valid` = FALSE WHERE `username` = ?", [username, ])
        return False
    elif (user_info["code"] != 200):
        return False
    else:
        send = False
        for module in user_info["data"]["modules"]:
            if (module["updated"]):
                send = True
        return send


if __name__ == '__main__':
    mysql = MySQL()
    to_check = mysql.query("SELECT * FROM `course` WHERE `valid`", [])

    for user in to_check:
        mail_test = check_and_send_mail(user)
        if mail_test:
            print("Send mail to course " + user[0])
            send_to = mysql.query("SELECT * FROM `subscription` WHERE `course` = ?", [user[0], ])
            for rec in send_to:
                send_html_mail(
                    rec[2], rec[1], "Dualis Parser - Grade may be Updated",
                    "Your course may have some new grades! <br> Check it out"
                )
