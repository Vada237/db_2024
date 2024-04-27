from flask import Flask


@app.route('/index')
def index():
    return 'hello world'
