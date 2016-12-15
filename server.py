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



# if __name__ == "__main__":
    
#     app.listen(8888)
#     tornado.ioloop.IOLoop.current().start()


def main():
    app = make_app()
    http_server = tornado.httpserver.HTTPServer(app)
    port = int(os.environ.get("PORT", 5000))
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()
 
if __name__ == "__main__":
    main()