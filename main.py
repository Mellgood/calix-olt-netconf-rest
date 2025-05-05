import os

from flask import Flask
from flask_restx import Api

from api.netconf.PonCosProfileAPI import init_pon_cos_profile_ns
from api.netconf.RunningConfigAPI import init_running_config_namespace
from model.netconf.NetconfSession import NetconfSession
from model.netconf.RunningConfig import RunningConfig
from model.netconf.ServiceAPI import init_service_namespace

app = Flask(__name__)
api = Api(app, title='Univaq API for calix E-7', version='1.0',
          description='This set of API enable to change parameters on the Calix E-7 device through a REST API.')

dev_env = os.getenv('DEV')
dev_env = False

running_config = None

if __name__ == '__main__':
    netconf_session = NetconfSession(host="10.13.17.60", port=830, username="sysadmin", password="sysadmin")

    if (dev_env):
        print("[WARNING]: We are running in dev mode. No interaction with the OLT!")
        f = open("running-config.xml")
        config_data = f.read().rstrip()
    else:
        config_data = netconf_session.netconf_get_config()

    if config_data is None:
        print("Errore: config_data is None")
        exit(1)
    else:
        running_config = RunningConfig(config_data)

        init_running_config_namespace(api, running_config)
        init_pon_cos_profile_ns(api, running_config)
        init_service_namespace(api)

    # init_pon_cos_profile_namespace(api, running_config)
    # init_running_config_namespace(api, running_config)

    # pc1 = running_config.get_pon_cos_profile(pon_cos_1)
    # print(pc1.get_bandwidth())
    # pc1.set_bandwidth(new_bw_type="explicit",new_max=4000000, new_min=4000000)

    # print(pc1.generate_netconf_payload())

    # netconf_session.netconf_edit_config(pc1.generate_netconf_payload(), "test1")

    app.run(debug=True, host='0.0.0.0', port=3333)
