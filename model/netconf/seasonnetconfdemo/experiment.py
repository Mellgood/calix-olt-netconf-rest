import argparse

import SS
import VOA
import PON
from ncclient import manager


def switch_configuration(config_type, mode):
    # Dettagli della connessione NETCONF per SS e PON
    pon_host = "10.13.17.60"
    pon_port = 830
    pon_username = "sysadmin"
    pon_password = "sysadmin"

    ss_host = "10.13.17.52"
    ss_port = 830
    ss_username = "admin"
    ss_password = "root"

    full_config_type = f"{config_type}_{mode}"

    if config_type == "2x1":
        # Configurazione 2x1 tramite SS
        SS.set_configuration(
            host=ss_host,
            port=ss_port,
            username=ss_username,
            password=ss_password,
            config_type=full_config_type
        )

        # Imposta attenuazione 300 tramite VOA
        VOA.set_attenuation(600)

        # Connessione al dispositivo PON tramite NETCONF
        try:
            with manager.connect(
                host=pon_host,
                port=pon_port,
                username=pon_username,
                password=pon_password,
                hostkey_verify=False
            ) as m:
                # Cancella ONT 1, ricrea ONT 1 e configura l'interfaccia 1/x1
                #PON.delete_ont1(m)
                #PON.create_ont1(m)
                PON.delete_ont(m, 1)
                PON.create_ont(m, 1, profile_id="801XGS", serial_number="47846E")
                PON.create_ont_eth_1x1(m)
                # Cancella ONT 2, ricrea ONT 2 e configura l'interfaccia 2/x1
                #PON.delete_ont2(m)
                #PON.create_ont2(m)
                PON.delete_ont(m, 2)
                PON.create_ont(m, 2, profile_id="801XGS", serial_number="478490")
                PON.create_ont_eth_2x1(m)
                # Spegne xp2
                PON.deactivate_xp2()

        except Exception as e:
            print(f"Errore durante la connessione PON NETCONF: {e}")

    elif config_type == "2x2":
        # Configurazione 2x2 tramite SS
        SS.set_configuration(
            host=ss_host,
            port=ss_port,
            username=ss_username,
            password=ss_password,
            config_type=full_config_type
        )

        # Imposta attenuazione 600 tramite VOA
        VOA.set_attenuation(900)

        # Attiva l'intefaccia xp2
        PON.activate_xp2()

        # Connessione al dispositivo PON tramite NETCONF
        try:
            with manager.connect(
                host=pon_host,
                port=pon_port,
                username=pon_username,
                password=pon_password,
                hostkey_verify=False
            ) as m:
                # Cancella ONT 1, ricrea ONT 1 e configura l'interfaccia 1/x1
                PON.delete_ont(m, 1)
                PON.create_ont(m, 1, profile_id="801XGS", serial_number="47846E")
                PON.create_ont_eth_1x1(m)
                # Cancella ONT 2, ricrea ONT 2 e configura l'interfaccia 2/x1
                PON.delete_ont(m, 2)
                PON.create_ont(m, 2, profile_id="801XGS", serial_number="478490")
                PON.create_ont_eth_2x1(m)

        except Exception as e:
            print(f"Errore durante la connessione PON NETCONF: {e}")

    else:
        print(f"Configurazione {config_type} non riconosciuta. Usa '2x1' o '2x2'.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Seleziona la configurazione PON e il tipo di connessione")

    parser.add_argument(
        '-c', '--config',
        type=str,
        required=True,
        choices=['2x1', '2x2'],
        help="Specifica la configurazione: '2x1' o '2x2'"
    )

    parser.add_argument(
        '-m', '--mode',
        type=str,
        choices=['b2b', 'mcf'],
        default='mcf',
        help="Specifica la modalità: 'b2b' o 'mcf' (default: 'mcf')"
    )

    args = parser.parse_args()

    switch_configuration(args.config, args.mode)

