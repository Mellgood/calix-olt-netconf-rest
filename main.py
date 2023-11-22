from flask import Flask
from flask_restx import Api
from api.config import ns as config_ns


from model.netconf.NetconfSession import NetconfSession

app = Flask(__name__)
api = Api(app, title='Config API', version='1.0', description='A simple API for configuration')

# Registrazione namespaces
api.add_namespace(config_ns, path='/running-config')


if __name__ == '__main__':
    #netconf_session = NetconfSession(host="10.10.10.30", port=22, username="sysadmin", password="sysadmin")
    app.run(debug=True, port=3333)