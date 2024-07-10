import tornado.ioloop
import tornado.web
from handlers import TaskHandler, SingleTaskHandler

def make_app():
    return tornado.web.Application([
        (r"/tasks", TaskHandler),
        (r"/tasks/([0-9]+)", SingleTaskHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
