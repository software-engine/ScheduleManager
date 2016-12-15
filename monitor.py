#!flask/bin/python
# encoding: utf-8

from datetime import date, datetime
import sqlite3
from email.mime.text import MIMEText
from config import Config
import smtplib
import time
import threading


def get_users():
    connect = sqlite3.connect('data.sqlite')
    bookmark_cursor = connect.execute("SELECT owner_id, activity_id FROM bookmark")
    owner = {}
    for row in bookmark_cursor:
        activity_cursor = connect.execute("SELECT start_date FROM activity WHERE id=?", row[1])
        for a_row in activity_cursor:
            d = datetime.strptime(a_row[0], '%Y-%m-%d').date()
            today = date.today()
            if (today - d).days == 1:
                owner.setdefault(int(row[0]))
    connect.close()
    return owner


def get_email(owner):
    connect = sqlite3.connect('data.sqlite')
    emails = []
    for user_id in owner.keys():
        user_cursor = connect.execute("SELECT email FROM user WHERE id=?", user_id)
        for email in user_cursor:
            emails.append(email)
    connect.close()
    return emails


def send_mail(emails):
    msg = MIMEText('the activities that you had marked will start soon, please check it out!', 'plain', 'utf-8')
    msg['From'] = Config.MAIL_USERNAME
    msg['Subject'] = 'activities notify'
    server = smtplib.SMTP(Config.MAIL_SERVER, Config.MAIL_PORT)
    server.login(Config.MAIL_USERNAME, Config.MAIL_PASSWORD)
    server.sendmail(Config.MAIL_USERNAME, emails, msg.as_string())
    server.quit()


def task():
    while True:
        users = get_users()
        emails = get_email(users)
        send_mail(emails)
        time.sleep(60 * 60)


def run_monitor():
    monitor = threading.Thread(target=task)
    monitor.start()


if __name__ == "__main__":
    run_monitor()
