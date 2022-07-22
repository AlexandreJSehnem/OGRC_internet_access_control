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
        file.close()
        self.loader = tornado.template.Loader("/home/dev/OGRC_internet_access_control/templates")
        super().__init__(application, request, **kwargs)

    def get(self):
        self.write(self.loader.load("login.html").generate())
        # self.write("Hello, world")

    def post(self, *args, **kwargs):
        user = self.get_body_argument("user")
        senha = self.get_body_argument("senha")
        file = open("auth", "r")
        count = 0
        print(user)
        print(senha)
        for line in file:
            line = line.replace("\n", "")
            print(line)
            if count == 0 and user == line:
                count += 1
                continue
            elif count == 1 and senha == line:
                count += 1
                continue
            else:
                self.write(self.loader.load("login.html").generate())
                return
        self.write(self.loader.load("manager.html").generate())



if __name__ == "__main__":
    application = tornado.web.Application([
        (r"/", MainHandler),
    ])
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()
