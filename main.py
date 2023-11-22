from flask import Flask
from flask_restx import Api

from api.netconf.PonCosProfileAPI import init_pon_cos_profile_ns
from api.netconf.RunningConfigAPI import init_running_config_namespace
from model.netconf.NetconfSession import NetconfSession
from model.netconf.RunningConfig import RunningConfig


app = Flask(__name__)
api = Api(app, title='Config API', version='1.0', description='A simple API for configuration')

running_config = None

if __name__ == '__main__':
    netconf_session = NetconfSession(host="10.10.10.30", port=830, username="sysadmin", password="sysadmin")
    config_data = netconf_session.netconf_get_config()
    #running_config = RunningConfig(config_data)

    if config_data is None:
        print("Errore: config_data è None")
    else:
        running_config = RunningConfig(config_data)

        if running_config is None:
            print("Errore: running_config è None")
        else:
            init_running_config_namespace(api, running_config)
            init_pon_cos_profile_ns(api, running_config)


    #init_pon_cos_profile_namespace(api, running_config)
    #init_running_config_namespace(api, running_config)

    #pc1 = running_config.get_pon_cos_profile(pon_cos_1)
    #print(pc1.get_bandwidth())
    #pc1.set_bandwidth(new_bw_type="explicit",new_max=4000000, new_min=4000000)

    #print(pc1.generate_netconf_payload())

    #netconf_session.netconf_edit_config(pc1.generate_netconf_payload(), "test1")


    app.run(debug=True, port=3333)
