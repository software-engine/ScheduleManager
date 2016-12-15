#!flask/bin/python
# encoding: utf-8

from flask_script import Manager, Shell
from app import create_app, db


app = create_app()
manager = Manager(app)
db.create_all(app=app)


def make_shell_context():
    return dict(db=db, app=app)
manager.add_command("shell", Shell(make_context=make_shell_context()))


if __name__ == '__main__':
    manager.run()
