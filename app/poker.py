from bottle import route, run
from poker_code import web_server

@route('/hello/<name>')
def index(name='World'):
    here = web_server()

    return '<b>Hello %s!</b>. It is %s right now.' % (name, here)

run(host='localhost', port=8080)
