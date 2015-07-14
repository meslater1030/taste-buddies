# -*- coding: utf-8 -*-


def app(environ, start_response):
    data = "Hello, World!\nHow are you?"
    start_response("200 OK", [
        ("Content-Type", "text/plain"),
        ("Content-Length", str(len(data)))
    ])
    return iter([data])

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('', 8080, app)
    srv.serve_forever()
