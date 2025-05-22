from ncclient import manager
import lxml.etree as ET


def get_existing_cross_connects(m):
    try:
        # Ottieni tutta la configurazione
        response = m.get_config(source='running').data_xml

        # Rimuovi la dichiarazione di encoding se presente
        response = response.encode('utf-8').decode('utf-8').split("?>", 1)[-1]

        # Esegui il parsing della risposta e filtra solo i cross-connects
        parsed_response = ET.fromstring(response)
        cross_connects = parsed_response.find(
            ".//{http://www.polatis.com/yang/optical-switch}cross-connects"
        )

        if cross_connects is not None:
            print("Existing Cross-Connects:")
            print(ET.tostring(cross_connects, pretty_print=True).decode())
        else:
            print("No existing cross-connects found.")

    except Exception as e:
        print("Failed to retrieve existing cross-connects:", e)


def create_cross_connect(m, ingress_port, egress_port):
    # XML configuration to create the cross-connect
    config = f"""
    <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
        <cross-connects xmlns="http://www.polatis.com/yang/optical-switch">
          <pair>
            <ingress>{ingress_port}</ingress>
            <egress>{egress_port}</egress>
          </pair>
        </cross-connects>
    </config>
    """

    # Send the configuration to the device
    try:
        response = m.edit_config(target='running', config=config)
        print(f"Cross-connect created successfully between ingress port {ingress_port} and egress port {egress_port}.")
    except Exception as e:
        print("Operation failed: ", e)
        if hasattr(e, 'xml'):
            print("Detailed Error: ")
            error_xml = ET.tostring(e._raw, pretty_print=True).decode()
            print(error_xml)


def set_configuration(host, port, username, password, config_type):
    with manager.connect(
            host=host,
            port=port,
            username=username,
            password=password,
            hostkey_verify=False
    ) as m:
        get_existing_cross_connects(m)

        if config_type == "2x2_b2b":
            print("Setting 2x2 configuration B2B...")
            create_cross_connect(m, 17, 21)
            create_cross_connect(m, 18, 22)
        elif config_type == "2x1_b2b":
            print("Setting 2x1 configuration B2B...")
            create_cross_connect(m, 17, 23)
            create_cross_connect(m, 19, 21)
            create_cross_connect(m, 20, 22)
        elif config_type == "2x2_mcf":
            print("Setting 2x2 configuration via MCF...")
            create_cross_connect(m, 17, 3)
            create_cross_connect(m, 18, 4)
            create_cross_connect(m, 21, 5)
            create_cross_connect(m, 22, 6)
        elif config_type == "2x1_mcf":
            print("Setting 2x1 configuration via MCF...")
            create_cross_connect(m, 17, 23)
            create_cross_connect(m, 19, 3)
            create_cross_connect(m, 20, 4)
            create_cross_connect(m, 21, 5)
            create_cross_connect(m, 22, 6)



        else:
            print("Invalid configuration type. Please use '2x2' or '2x1'.")

if __name__ == '__main__':
    # Esempio di utilizzo
    set_configuration(
        host="10.13.17.52",
        port=830,
        username="admin",
        password="root",
        config_type="2x2"  # Modifica con "2x2" per l'altra configurazione
    )
