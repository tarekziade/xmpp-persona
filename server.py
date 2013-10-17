import os
from bottle import route, run, template, static_file

STATIC = os.path.abspath(os.path.join(os.path.dirname(__file__), 'example'))


@route('/<filename:path>')
def index(filename):
    return static_file(filename, root=STATIC)


run(host='localhost', port=8080)
