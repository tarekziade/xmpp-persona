import os
import bottle
from bottle import (route, run, template, static_file, redirect,
                    request, template)
import browserid
import beaker.middleware

session_opts = {
    'session.type': 'file',
    'session.data_dir': './session/',
    'session.auto': True,
    }

STATIC = os.path.abspath(os.path.join(os.path.dirname(__file__), 'example'))

verifier = browserid.LocalVerifier(['*'])
app = beaker.middleware.SessionMiddleware(bottle.app(), session_opts)


@route('/<filename:path>')
def static(filename):
    return static_file(filename, root=STATIC)


@route('/basic.html')
def index():
    with open(os.path.join(STATIC, 'basic.html')) as f:
        data = f.read()

    session = request.environ.get('beaker.session')
    return template(data, session=session)


@route('/login', method='POST')
def login():
    assertion = request.POST['assertion']
    try:
        data = verifier.verify(assertion, '*')
        email = data['email']
        app_session = request.environ.get('beaker.session')
        app_session['logged_in'] = True
        app_session['email'] = email
        app_session['assertion'] = assertion
    except ValueError, UnicodeDecodeError:
        # need to raise a auth
        pass
    return {'email': email}


@route('/logout', method='POST')
def logout():
    app_session = request.environ.get('beaker.session')
    app_session['logged_in'] = False
    app_session['email'] = None
    redirect("/basic.html")


@route('/')
def _index():
    redirect("/basic.html")



run(host='localhost', port=8080, app=app)
