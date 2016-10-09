from random import randint
from time import sleep
from wsgiref.simple_server import make_server

def events(max_delay, limit):
    while True:
        delay = randint(1, max_delay)
        if delay >= limit:
            sleep(limit)
            yield None
        else:
            sleep(delay)
            yield 'Event generated, awaiting %d s' % delay

generator = events(4, 2)

class WSGIApplication:
    def __init__(self, environment, start_response):
        print('GET request')
        self.environment = environment
        self.start_response = start_response
        self.headers = [
            ('Content-type', 'text/plain; charset=utf-8')
        ]

    def __iter__(self):
        if self.environment.get('PATH_INFO', '/') == '/':
            yield from self.ok_response(generator.__next__())
        else:
            self.not_found_response()
            print('Done')

    def not_found_response(self):
        self.start_response('404 Not Found', self.headers)

    def ok_response(self, message):
        print (message)
        if message:
            self.start_response('200 OK', self.headers)
            yield ('%s\n' % message).encode('utf-8')
        else:
            self.start_response('204 NO CONTENT', self.headers)
            yield ('%s\n' % "Error").encode('utf-8')


if __name__ == '__main__':
    server = make_server('127.0.0.1', 3000, WSGIApplication)
    server.serve_forever()

