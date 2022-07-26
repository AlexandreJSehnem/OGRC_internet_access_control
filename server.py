# import easy_get_set
from tornado import httputil
import tornado.ioloop
import tornado.web
import tornado.template
import easy_get_set

PORT = '1.3.6.1.2.1.2.2.1.7.'


class MainHandler(tornado.web.RequestHandler):

    def __init__(self, application, request: httputil.HTTPServerRequest, **kwargs) -> None:
        self.snmp_handler = easy_get_set.snMPP()
        file = open("ports", "w")
        self.port_list_1 = {}
        self.port_list_2 = {}
        for index in range(5):
            single_port = PORT+str(index+1)
            port_status = self.snmp_handler.get(single_port)[-1][1]
            # file.write(str(single_port)+" "+str(port_status))
            self.port_list_1[str(single_port)] = [int(port_status), index+1]  # port_status
        for index2 in range(5, 10):
            single_port = PORT+str(index2+1)
            port_status = self.snmp_handler.get(single_port)[-1][1]
            # file.write(str(single_port)+" "+str(port_status))
            self.port_list_2[str(single_port)] = [int(port_status), index2+1]  # port_status
        file.close()
        self.loader = tornado.template.Loader(
            "./templates")
        super().__init__(application, request, **kwargs)

    def get(self):
        self.write(self.loader.load("login.html").generate())

    def post(self, *args, **kwargs):
        user = self.get_body_argument("user", None)
        senha = self.get_body_argument("senha", None)
        manage = self.get_body_argument("form", None)
        if manage:
            for i in range(1, 6):
                status = self.get_body_argument(str(i), None)
                if status:
                    if status == "Ligado":
                        port_oid = PORT + str(i)
                        print(port_oid)
                        self.port_list_1[port_oid][0] = 0
                        self.snmp_handler.set(port_oid, 2)
                    elif status == "Desligado":
                        port_oid = PORT + str(i)
                        self.port_list_1[port_oid][0] = 1
                        self.snmp_handler.set(port_oid, 1)
            for j in range(6, 11):
                status = self.get_body_argument(str(j), None)
                if status:
                    if status == "Ligado":
                        port_oid = PORT + str(j)
                        print(port_oid)
                        self.port_list_2[port_oid][0] = 0
                        self.snmp_handler.set(port_oid, 2)
                    elif status == "Desligado":
                        port_oid = PORT + str(j)
                        self.port_list_2[port_oid][0] = 1
                        self.snmp_handler.set(port_oid, 1)
            self.write(self.loader.load("manager.html").generate(ports=self.port_list_1, ports2=self.port_list_2))
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
                file.close()
                self.write(self.loader.load("login.html").generate())
                return
        file.close()
        self.write(self.loader.load("manager.html").generate(ports=self.port_list_1, ports2=self.port_list_2))


if __name__ == "__main__":
    application = tornado.web.Application([
        (r"/", MainHandler),
    ])
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()
