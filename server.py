import tornado.ioloop
import tornado.web
import os
from johnJanssonKlaparesDag import *


class MainHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        self.render('templates/index.html', result=result)


def make_app():

    settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "debug": True,
    }

    return tornado.web.Application([
        (r'/', MainHandler),
        (r'/static/(.*)', tornado.web.StaticFileHandler, dict(path=settings['static_path'])),
    ], **settings)



if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()