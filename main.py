import os

from flask import Flask
from flask_restx import Api

from api.netconf.InventoryAPI import init_inventory_namespace
from api.netconf.PonCosProfileAPI import init_pon_cos_profile_ns
from api.netconf.RunningConfigAPI import init_running_config_namespace
from api.netconf.TopologyAPI import init_topology_namespace
from model.netconf.NetconfSession import NetconfSession
from model.netconf.RunningConfig import RunningConfig
from model.netconf.ServiceAPI import init_service_namespace

app = Flask(__name__)
api = Api(app, title='Univaq API for calix E-7', version='1.0',
          description='This set of API enables changing parameters on the Calix E-7 device through a REST API.')

dev_env = os.getenv('DEV')

running_config = None

if __name__ == '__main__':
    netconf_session = NetconfSession(host="10.30.7.6", port=830, username="sysadmin", password="sysadmin")

    if dev_env:
        print("[WARNING]: We are running in dev mode. No interaction with the OLT!")

        # Verifica se il file 'running-config.xml' esiste
        if not os.path.exists("running-config.xml"):
            print("File 'running-config.xml' non trovato. Recupero configurazione dal dispositivo...")
            config_data = netconf_session.netconf_get_config()  # Recupera la configurazione tramite NETCONF

            if config_data is None:
                print("Errore: non è stato possibile recuperare la configurazione dal dispositivo.")
                exit(1)

            # Estrai il contenuto XML dalla risposta NETCONF
            config_str = config_data.xml

            # Salva la configurazione recuperata nel file
            with open("running-config.xml", "w") as f:
                f.write(config_str)  # Scrivi la configurazione come stringa XML
                print("Configurazione salvata in 'running-config.xml'.")
        else:
            # Carica la configurazione dal file esistente
            with open("running-config.xml", "r") as f:
                config_data = f.read().rstrip()
                print("File 'running-config.xml' trovato. Caricamento configurazione.")

    else:
        # Recupera la configurazione dal dispositivo in modalità produzione
        config_data = netconf_session.netconf_get_config()

    if config_data is None:
        print("Errore: config_data is None")
        exit(1)
    else:
        running_config = RunningConfig(config_data)

        # Inizializza i namespace per le risorse API
        init_running_config_namespace(api, running_config)
        init_pon_cos_profile_ns(api, running_config)
        init_service_namespace(api)
        init_inventory_namespace(api)
        init_topology_namespace(api)

    # Avvio dell'app Flask
    app.run(debug=True, host='0.0.0.0', port=3333)
