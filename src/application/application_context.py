import tornado.ioloop
import tornado.web

import motor

# import ui templates
# from view import partials

# import controllers
from clean.clean_service.src.controller.process import CleaningProcessHandler


class ApplicationContext(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/cleaning-process/([^/]+)?", CleaningProcessHandler)
        ]

        settings = dict(
            db=motor.motor_tornado.MotorClient(
                'mongodb://localhost:27017'
            ).genomeInput
            # xsrf_cookies=True,
            # cookie_secret='123456789',
            # login_url='/login'
        )

        tornado.web.Application.__init__(self, handlers, **settings)
