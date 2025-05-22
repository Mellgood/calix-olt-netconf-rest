from ncclient import manager
from lxml import etree

# Dati di connessione al dispositivo
host = "10.10.10.30"  # Sostituisci con l'indirizzo IP del tuo dispositivo
port = 830            # Porta NETCONF
username = "sysadmin" # Nome utente per l'autenticazione
password = "sysadmin" # Password per l'autenticazione

# XML del comando NETCONF per eseguire il reset dell'ONT 1
netconf_reset_ont = '''
<action xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="101">
  <reset-ont xmlns="http://www.calix.com/ns/exa/gpon-interface-base">
    <ont-id>1</ont-id>
  </reset-ont>
</action>
'''

# Funzione per eseguire il reset dell'ONT 1
def reset_ont(m):
    try:
        # Converti il comando XML in un oggetto XML valido per NETCONF
        netconf_command = etree.fromstring(netconf_reset_ont)
        # Invia il comando con dispatch
        response = m.dispatch(netconf_command)
        print("Reset dell'ONT 1 eseguito.")
        print(response)
    except Exception as e:
        print(f"Errore durante l'esecuzione del reset dell'ONT 1: {e}")

# Funzione principale per eseguire l'operazione di reset
def main():
    try:
        # Connessione al dispositivo tramite NETCONF
        with manager.connect(
            host=host,
            port=port,
            username=username,
            password=password,
            hostkey_verify=False
        ) as m:
            # Eseguire il reset dell'ONT 1
            reset_ont(m)

    except Exception as e:
        print(f"Errore durante la connessione al dispositivo: {e}")

# Esecuzione dello script
if __name__ == '__main__':
    main()
