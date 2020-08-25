from flask import Flask, current_app

from common.models.user import User
from lawyer import create_app

app = create_app()


@app.route('/')
def hello_word():

    print(User.query.all())
    return "hello word", 400


if __name__ == '__main__':
    app.run(debug=True)
