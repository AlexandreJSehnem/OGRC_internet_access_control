import easy_get_set
from flask import Flask

s = easy_get_set.snMPP()
app = Flask(__name__)


@app.route('/get/<int:eth_port>')
def rest_get_port_status(eth_port: int):
    print("GET ETHERNET PORT STATUS")
    r = s.get(OID=('1.3.6.1.2.1.2.2.1.7.'+str(eth_port)))
    return str(r[-1][1])


@app.route('/set/<int:eth_port>/<int:value>')
def rest_set_port_status(eth_port: int, value: int):
    r = s.set(OID=('1.3.6.1.2.1.2.2.1.7.'+str(eth_port)),
              value=value)
    return str(r)


@app.route('/get/mac/<int:eth_port>')
def rest_get_mac(eth_port: int):
    r = s.get(OID=('1.3.6.1.2.1.4.22.1.2.')+str(eth_port))
    print(r)
    return str(r)


if(__name__ == '__main__'):
    app.run()
