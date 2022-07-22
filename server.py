# import easy_get_set
from tornado import httputil
import tornado.ioloop
import tornado.web
import tornado.template
# import tornado.httpclient as httpclient
PORT = '1.3.6.1.2.1.2.2.1.7.'


class MainHandler(tornado.web.RequestHandler):

    def __init__(self, application, request: httputil.HTTPServerRequest, **kwargs) -> None:
        # self.snmp_handler = easy_get_set.snMPP()
        file = open("ports", "w")
        self.port_list = {}
        for index in range(15):
            single_port = PORT+str(index+1)
            # port_status = self.snmp_handler.get(single_port)
            # file.write(str(single_port)+" "+str(port_status))
            self.port_list[str(single_port)] = 1  # port_status
        print(self.port_list)
        super().__init__(application, request, **kwargs)

    def get(self):
        loader = tornado.template.Loader("/home/dev/OGRC_internet_access_control/templates")
        self.write(loader.load("switch.html").generate())
        # self.write("Hello, world")

    def post(self, *args, **kwargs):
        print("oh man")
        code = 404
        self.set_status(code)
        self.finish({'Error:': 'Just a test', 'Code': code, 'reason': 'Really, its just a test'})


if __name__ == "__main__":
    application = tornado.web.Application([
        (r"/", MainHandler),
    ])
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()
