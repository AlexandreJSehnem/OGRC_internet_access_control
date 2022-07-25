# import easy_get_set
from tornado import httputil
import tornado.ioloop
import tornado.web
import tornado.template

PORT = '1.3.6.1.2.1.2.2.1.7.'


class MainHandler(tornado.web.RequestHandler):

    def __init__(self, application, request: httputil.HTTPServerRequest, **kwargs) -> None:
        self.snmp_handler = easy_get_set.snMPP()
        file = open("ports", "w")
        self.port_list = {}
        for index in range(15):
            single_port = PORT+str(index+1)
            port_status = self.snmp_handler.get(single_port)
            # file.write(str(single_port)+" "+str(port_status))
            self.port_list[str(single_port)] = [int(port_status), index+1]  # port_status
        file.close()
        self.loader = tornado.template.Loader("/home/dev/OGRC_internet_access_control/templates")
        super().__init__(application, request, **kwargs)

    def get(self):
        self.write(self.loader.load("login.html").generate())

    def post(self, *args, **kwargs):
        user = self.get_body_argument("user", None)
        senha = self.get_body_argument("senha", None)
        if not user and not senha:
            for i in range(1, 16):
                status = self.get_body_argument(str(i), None)
                if status:
                    if status == "Ligado":
                        port_oid = PORT + str(i)
                        self.port_list[port_oid][0] = 0
                        self.snmp_handler.set(port_oid, 0)
                    elif status == "Desligado":
                        port_oid = PORT + str(i)
                        self.port_list[port_oid][0] = 1
                        self.snmp_handler.set(port_oid, 1)
            self.write(self.loader.load("manager.html").generate(ports=self.port_list))
            return
        file = open("auth", "r")
        count = 0
        for line in file:
            line = line.replace("\n", "")
            if count == 0 and user == line:
                count += 1
                continue
            elif count == 1 and senha == line:
                count += 1
                continue
            else:
                self.write(self.loader.load("login.html").generate())
                return
        self.write(self.loader.load("manager.html").generate(ports=self.port_list))


if __name__ == "__main__":
    application = tornado.web.Application([
        (r"/", MainHandler),
    ])
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()
