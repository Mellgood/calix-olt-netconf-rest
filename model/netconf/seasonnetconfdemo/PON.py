import subprocess
from re import sub

import paramiko, time


from lxml import etree
from ncclient import manager
from ncclient.operations import RPCError



# Dati di connessione al dispositivo
host = "10.30.7.6"  # Sostituisci con l'indirizzo IP del tuo dispositivo
port = 830            # Porta NETCONF
username = "sysadmin" # Nome utente per l'autenticazione
password = "sysadmin" # Password per l'autenticazione

# XML per cancellare l'ONT 2
netconf_delete_ont2 = '''
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <config xmlns="http://www.calix.com/ns/exa/base">
    <system>
      <ont xmlns="http://www.calix.com/ns/exa/gpon-interface-base"
           nc:operation="delete"
           xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
        <ont-id>2</ont-id>
      </ont>
    </system>
  </config>
</config>
'''
# XML per cancellare l'ONT 1
netconf_delete_ont1 = '''
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <config xmlns="http://www.calix.com/ns/exa/base">
    <system>
      <ont xmlns="http://www.calix.com/ns/exa/gpon-interface-base"
           nc:operation="delete"
           xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
        <ont-id>1</ont-id>
      </ont>
    </system>
  </config>
</config>
'''

# XML per creare l'ONT 1
netconf_create_ont1 = '''
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <config xmlns="http://www.calix.com/ns/exa/base">
    <system>
      <ont xmlns="http://www.calix.com/ns/exa/gpon-interface-base">
        <ont-id>1</ont-id>
        <profile-id>801XGS</profile-id>
        <serial-number>47846E</serial-number>
      </ont>
    </system>
  </config>
</config>
'''

# XML per creare l'ONT 2
netconf_create_ont2 = '''
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <config xmlns="http://www.calix.com/ns/exa/base">
    <system>
      <ont xmlns="http://www.calix.com/ns/exa/gpon-interface-base">
        <ont-id>2</ont-id>
        <profile-id>801XGS</profile-id>
        <serial-number>478490</serial-number>
      </ont>
    </system>
  </config>
</config>
'''

# XML per creare l'interfaccia ont-ethernet 2/x1
netconf_create_ont_eth_2x1 = '''
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
    <interface>
      <name>2/x1</name>
      <ont-ethernet xmlns="http://www.calix.com/ns/exa/gpon-interface-std">
        <role>uni</role>
        <l2cp-action>tunnel</l2cp-action>
        <vlan>
          <vlan-id>333</vlan-id>
          <policy-map>
            <name>ELINE_PM_2</name>
            <class-map-ethernet>
              <name>Eth-match-any-2</name>
              <ingress>
                <meter-type>meter-mef</meter-type>
              </ingress>
            </class-map-ethernet>
          </policy-map>
        </vlan>
      </ont-ethernet>
    </interface>
  </interfaces>
</config>
'''

# XML per creare l'interfaccia ont-ethernet 1/x1
netconf_create_ont_eth_1x1 = '''
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
    <interface>
      <name>1/x1</name>
      <ont-ethernet xmlns="http://www.calix.com/ns/exa/gpon-interface-std">
        <role>uni</role>
        <l2cp-action>tunnel</l2cp-action>
        <vlan>
          <vlan-id>222</vlan-id>
          <policy-map>
            <name>ELIN_PM_1</name>
            <class-map-ethernet>
              <name>Eth-match-any-1</name>
              <ingress>
                <meter-type>meter-mef</meter-type>
              </ingress>
            </class-map-ethernet>
          </policy-map>
        </vlan>
      </ont-ethernet>
    </interface>
  </interfaces>
</config>
'''

def strip_xml_decl(xml_string):
    # Rimuove "<?xml ...?>" se presente
    return sub(r'^<\?xml[^>]+\?>\s*', '', xml_string)


# Funzione per cancellare ONT 2
def delete_ont2(m):
    try:
        response = m.edit_config(netconf_delete_ont2, target="running")
        print("ONT 2 cancellata.")
        print(response)
    except Exception as e:
        print(f"Errore durante la cancellazione dell'ONT 2: {e}")

# Funzione per cancellare ONT 1
def delete_ont1(m):
    try:
        response = m.edit_config(netconf_delete_ont1, target="running")
        print("ONT 1 cancellata.")
        print(response)
    except Exception as e:
        print(f"Errore durante la cancellazione dell'ONT 1: {e}")

# Funzione per creare ONT 2
def create_ont2(m):
    try:
        response = m.edit_config(netconf_create_ont2, target="running")
        print("ONT 2 creata.")
        print(response)
    except Exception as e:
        print(f"Errore durante la creazione dell'ONT 2: {e}")

# Funzione per creare ONT 1
def create_ont1(m):
    try:
        response = m.edit_config(netconf_create_ont1, target="running")
        print("ONT 1 creata.")
        print(response)
    except Exception as e:
        print(f"Errore durante la creazione dell'ONT 1: {e}")

# Funzione per creare l'interfaccia ont-ethernet 2/x1
def create_ont_eth_2x1(m):
    try:
        response = m.edit_config(netconf_create_ont_eth_2x1, target="running")
        print("Interfaccia 2/x1 creata.")
        print(response)
    except Exception as e:
        print(f"Errore durante la creazione dell'interfaccia 2/x1: {e}")

# Funzione per creare l'interfaccia ont-ethernet 1/x1
def create_ont_eth_1x1(m):
    try:
        response = m.edit_config(netconf_create_ont_eth_1x1, target="running")
        print("Interfaccia 1/x1 creata.")
        print(response)
    except Exception as e:
        print(f"Errore durante la creazione dell'interfaccia 1/x1: {e}")


def create_vlan(m, vlan_id, mode="ELINE"):
    """
    Crea (o fonde, se già esistente) una VLAN nel sistema,
    assegnandole l'ID e il mode desiderati.
    """

    # Qui usiamo nc:operation="merge" così:
    # - se la VLAN non esiste, la crea.
    # - se la VLAN esiste, ne aggiorna i campi senza cancellare altre impostazioni.
    # Se preferisci forzare la creazione, usa "create" (ma va in errore se esiste già).

    netconf_create_vlan = f"""
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <config xmlns="http://www.calix.com/ns/exa/base">
    <system>
      <vlan xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" nc:operation="merge">
        <vlan-id>{vlan_id}</vlan-id>
        <mode>{mode}</mode>
      </vlan>
    </system>
  </config>
</config>
"""
    try:
        response = m.edit_config(target='running', config=netconf_create_vlan)
        print(f"VLAN {vlan_id} creata/aggiornata con mode {mode}.")
        print(response)
    except Exception as e:
        print(f"Errore durante la creazione/aggiornamento della VLAN {vlan_id}: {e}")

def add_vlan_to_general_tsp(m, vlan_id):

    # Esattamente la struttura che Netconf Explorer ha mostrato
    xml_snippet = f"""
<config>
  <!-- Questo <config> è quello "netconf" generico. 
       ncclient lo metterà DENTRO <edit-config><config>... -->
  <config xmlns="http://www.calix.com/ns/exa/base">
    <!-- Questo <config> invece è nel namespace Calix e
         contiene <profile> e <transport-service-profile>. -->
    <profile>
      <transport-service-profile>
        <tsp-name>GENERAL_TSP{vlan_id}</tsp-name>
        <vlan-list>{vlan_id}</vlan-list>
      </transport-service-profile>
    </profile>
  </config>
</config>
"""

    try:
        response = m.edit_config(target="running", config=xml_snippet)
        print("Risposta:", response)
    except Exception as e:
        print(f"Errore: {e}")

def create_class_map_ethernet_match_any(m, ont_id):

    # Esattamente la struttura che Netconf Explorer ha mostrato
    xml_snippet = f"""
<config>
  <!-- Questo <config> è quello "netconf" generico. 
       ncclient lo metterà DENTRO <edit-config><config>... -->
  <config xmlns="http://www.calix.com/ns/exa/base">
    <!-- Questo <config> invece è nel namespace Calix e
         contiene <profile> e <transport-service-profile>. -->
    <profile>
      <class-map>
        <ethernet>
          <name>Eth-match-any-{ont_id}</name>
          <flow>
            <flow-index>1</flow-index>
            <rule>
              <index>1</index>
              <match>
                <any>true</any>
              </match>
            </rule>
          </flow>
        </ethernet>
      </class-map>
    </profile>
  </config>
</config>
"""

    try:
        response = m.edit_config(target="running", config=xml_snippet)
        print("Risposta:", response)
    except Exception as e:
        print(f"Errore: {e}")

def create_policy_map_eline(m, ont_id):

    # Esattamente la struttura che Netconf Explorer ha mostrato
    xml_snippet = f"""
<config>
  <!-- Questo <config> è quello "netconf" generico. 
       ncclient lo metterà DENTRO <edit-config><config>... -->
  <config xmlns="http://www.calix.com/ns/exa/base">
    <!-- Questo <config> invece è nel namespace Calix e
         contiene <profile> e <transport-service-profile>. -->
    <profile>
      <policy-map>
        <name>ELINE_PM_{ont_id}</name>
        <class-map-ethernet>
          <name>Eth-match-any-{ont_id}</name>
          <ingress>
            <meter-type>meter-mef</meter-type>
            <eir>10000000</eir>
          </ingress>
        </class-map-ethernet>
      </policy-map>
    </profile>
  </config>
</config>
"""

    try:
        response = m.edit_config(target="running", config=xml_snippet)
        print("Risposta:", response)
    except Exception as e:
        print(f"Errore: {e}")

def create_pon_cos_profile_be(m, ont_id):

    # Esattamente la struttura che Netconf Explorer ha mostrato
    xml_snippet = f"""
<config>
  <!-- Questo <config> è quello "netconf" generico. 
       ncclient lo metterà DENTRO <edit-config><config>... -->
  <config xmlns="http://www.calix.com/ns/exa/base">
    <!-- Questo <config> invece è nel namespace Calix e
         contiene <profile> e <transport-service-profile>. -->
    <profile>
      <pon-cos-profile xmlns="http://www.calix.com/ns/exa/gpon-interface-base">
        <name>ont_{ont_id}_be</name>
        <prio>4</prio>
      </pon-cos-profile>
    </profile>
  </config>
</config>
"""

    try:
        response = m.edit_config(target="running", config=xml_snippet)
        print("Risposta:", response)
    except Exception as e:
        print(f"Errore: {e}")

def create_pon_cos_profile_ef(m, ont_id,bandwidth):

    # Esattamente la struttura che Netconf Explorer ha mostrato
    xml_snippet = f"""
<config>
  <!-- Questo <config> è quello "netconf" generico. 
       ncclient lo metterà DENTRO <edit-config><config>... -->
  <config xmlns="http://www.calix.com/ns/exa/base">
    <!-- Questo <config> invece è nel namespace Calix e
         contiene <profile> e <transport-service-profile>. -->
    <profile>
      <pon-cos-profile xmlns="http://www.calix.com/ns/exa/gpon-interface-base">
        <name>ont_{ont_id}_ef</name>
        <prio>4</prio>
        <bw>
          <type>explicit</type>
          <maximum>{bandwidth}</maximum>
          <minimum>{bandwidth}</minimum>
        </bw>
        <cos-type>expedited</cos-type>
      </pon-cos-profile>
    </profile>
  </config>
</config>
"""

    try:
        response = m.edit_config(target="running", config=xml_snippet)
        print("Risposta:", response)
    except Exception as e:
        print(f"Errore: {e}")

def create_interface_ont_ethernet(m, ont_id, ethernet_interface, s_vlan):
    # Costruiamo esattamente la struttura che Netconf Explorer usa
    xml_snippet = f"""
<config>
  <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
    <interface>
      <name>{ont_id}/x{ethernet_interface}</name>
      <ont-ethernet xmlns="http://www.calix.com/ns/exa/gpon-interface-std">
        <role>uni</role>
        <l2cp-action>tunnel</l2cp-action>
        <vlan>
          <vlan-id>{s_vlan}</vlan-id>
          <policy-map>
            <name>ELINE_PM_{ont_id}</name>
            <class-map-ethernet>
              <name>Eth-match-any-{ont_id}</name>
              <ingress>
                <meter-type>meter-mef</meter-type>
              </ingress>
            </class-map-ethernet>
          </policy-map>
        </vlan>
      </ont-ethernet>
    </interface>
  </interfaces>
</config>
"""

    try:
        response = m.edit_config(target="running", config=xml_snippet)
        print("Risposta:", response)
    except Exception as e:
        print(f"Errore: {e}")

def apply_pon_cos_profile_be(m, ont_id):
    # Costruiamo l'XML replicando la struttura
    # di <edit-config> che funziona da Netconf Explorer.
    # N.B.: ncclient aggiunge già il blocco <edit-config> esterno, perciò
    #       noi costruiamo solo <config> ... <config> ...
    xml_snippet = f"""
<config>
    <config xmlns="http://www.calix.com/ns/exa/base">
      <system>
        <ont xmlns="http://www.calix.com/ns/exa/gpon-interface-base">
          <ont-id>{ont_id}</ont-id>
          <pon-us-cos>
            <index>user-1</index>
            <!-- Puoi parametrizzare il profilo se serve -->
            <pon-us-cos-profile>ont_{ont_id}_be</pon-us-cos-profile>
          </pon-us-cos>
        </ont>
      </system>
    </config>
</config>
"""

    try:
        response = m.edit_config(target="running", config=xml_snippet)
        print("Risposta:", response)
    except Exception as e:
        print(f"Errore: {e}")

def apply_pon_cos_profile_ef(m, ont_id):
    # Costruiamo l'XML replicando la struttura
    # di <edit-config> che funziona da Netconf Explorer.
    # N.B.: ncclient aggiunge già il blocco <edit-config> esterno, perciò
    #       noi costruiamo solo <config> ... <config> ...
    xml_snippet = f"""
<config>
    <config xmlns="http://www.calix.com/ns/exa/base">
      <system>
        <ont xmlns="http://www.calix.com/ns/exa/gpon-interface-base">
          <ont-id>{ont_id}</ont-id>
          <pon-us-cos>
            <index>user-1</index>
            <!-- Puoi parametrizzare il profilo se serve -->
            <pon-us-cos-profile>ont_{ont_id}_ef</pon-us-cos-profile>
          </pon-us-cos>
        </ont>
      </system>
    </config>
</config>
"""

    try:
        response = m.edit_config(target="running", config=xml_snippet)
        print("Risposta:", response)
    except Exception as e:
        print(f"Errore: {e}")

def activate_ethernet(m, port_number, vlan_id):
    # Costruiamo l'XML che replichi la struttura di Netconf Explorer
    xml_snippet = f"""
<config>
  <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
    <interface>
      <name>1/1/x{port_number}</name>
      <enabled>true</enabled>
      <ethernet xmlns="http://www.calix.com/ns/ethernet-std">
        <role>inni</role>
        <native-vlan>999</native-vlan>
        <transport-service-profile>GENERAL_TSP{vlan_id}</transport-service-profile>
      </ethernet>
    </interface>
  </interfaces>
</config>
"""
    try:
        response = m.edit_config(target="running", config=xml_snippet)
        print("Risposta:", response)
    except Exception as e:
        print(f"Errore: {e}")



def create_service(m, ont_id, cvlan, ethernet_port, svlan, profile, bw=None):
    """
    - ASSUME ont già esistenti e interfacce ethernet in no-shutdown
    Crea e configura un servizio su una ONT, comprendendo:
      - Creazione VLAN e aggiunta al TSP (Transport Service Profile)
      - Configurazione class-map e policy-map
      - Creazione e applicazione del cos-profile (BE o EF)
      - Attivazione dell'interfaccia Ethernet

    Parametri:
      m               : sessione ncclient
      ont_id         : ID dell'ONT su cui operare
      cvlan          : (se richiesto) id della Customer VLAN
      ethernet_port  : la porta Ethernet dell'ONT (es. 1/1/x1) o simile
      svlan          : Service VLAN da configurare
      profile        : "bw" (Best Effort) o "ef" (Expedited Forwarding)
      bw             : opzionale, larghezza di banda da impostare (richiesto se profile == "ef")
    """
    ##TODO: aggiustare controllo sulla banda
    if ethernet_port == "1":
        print("Activting xp1")
        activate_xp1()
        create_ont(m, 1, profile_id="801XGS", serial_number="47846E")
    if ethernet_port == "2":
        print("Activting xp2")
        activate_xp2()
        create_ont(m, 2, profile_id="801XGS", serial_number="478490")


    # 1) Creazione VLAN (se necessario) - usiamo la S-VLAN
    create_vlan(m, svlan)

    # 2) Aggiunta VLAN al "general_tsp" (o a un TSP specifico)
    add_vlan_to_general_tsp(m, svlan)

    # 7) Attivazione della porta Ethernet
    activate_ethernet(m, ethernet_port, svlan)

    # 3) Creazione class-map Ethernet "match-any" per la ONT
    create_class_map_ethernet_match_any(m, ont_id)

    # 4) Creazione policy-map ELINE
    create_policy_map_eline(m, ont_id)


    # 5) Creazione e configurazione dell'interfaccia ONT Ethernet
    create_interface_ont_ethernet(m, ont_id, 1, svlan)

    # 6) In base al profilo richiesto, crea e applica i cos-profile
    if profile == "be":
        # Esempio: usiamo la nomenclatura "be" = best effort
        create_pon_cos_profile_be(m, ont_id)
        apply_pon_cos_profile_be(m, ont_id)
    elif profile == "ef":
        # Qui bw è obbligatorio
        if bw is None:
            raise ValueError("È necessario specificare 'bw' quando profile='ef'")

        create_pon_cos_profile_ef(m, ont_id, bw)
        apply_pon_cos_profile_ef(m, ont_id)
    else:
        raise ValueError("Valore di 'profile' non riconosciuto. Usa 'be' o 'ef'.")


def delete_vlan(m, svlan):
    config = f'''
    <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
      <vlan xmlns="http://www.calix.com/ns/exa/gpon-interface-base" nc:operation="delete"
            xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
        <name>{svlan}</name>
      </vlan>
    </config>
    '''
    return m.edit_config(config=config, target="running").xml

def remove_vlan_from_general_tsp(m, svlan):
    config = f'''
    <config>
      <tsp xmlns="http://www.calix.com/ns/exa/gpon-interface-base">
        <name>general_tsp</name>
        <vlan-list nc:operation="delete"
            xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
          <vlan>{svlan}</vlan>
        </vlan-list>
      </tsp>
    </config>
    '''
    return m.edit_config(config=config, target="running").xml

def delete_class_map_ethernet_match_any(m, ont_id):
    name = f"Eth-match-any-{ont_id}"
    config = f"""
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <config xmlns="http://www.calix.com/ns/exa/base">
    <profile>
      <class-map>
        <ethernet nc:operation="delete"
                  xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
          <name>{name}</name>
        </ethernet>
      </class-map>
    </profile>
  </config>
</config>
"""
    return m.edit_config(config=config, target="running").xml

def delete_policy_map_eline(m, ont_id):
    name = f"ELINE_PM_{ont_id}"
    config = f"""
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <config xmlns="http://www.calix.com/ns/exa/base">
    <profile>
      <policy-map nc:operation="delete"
                  xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
        <name>{name}</name>
      </policy-map>
    </profile>
  </config>
</config>
"""

    print("===== DELETE POLICY MAP REQUEST =====")
    print(config)
    print("=====================================")

    try:
        response = m.edit_config(target="running", config=config)
        print("✔️ DELETE SUCCESS:", response)
        return response.xml
    except RPCError as rpc_err:
        print("❌ RPCError during delete_policy_map_eline:")
        print(rpc_err)
        raise
    except Exception as exc:
        print("❌ Unexpected error during delete_policy_map_eline:")
        print(exc)
        raise


def delete_interface_ont_ethernet(m, interface_name):
    config = f'''
<config>
  <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
    <interface nc:operation="delete"
               xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
      <name>{interface_name}</name>
    </interface>
  </interfaces>
</config>
'''
    return m.edit_config(config=config, target="running").xml

def deactivate_ethernet(m, port_number):
    xml_snippet = f"""
<config>
  <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
    <interface>
      <name>1/1/x{port_number}</name>
      <enabled>false</enabled>
    </interface>
  </interfaces>
</config>
"""
    return m.edit_config(config=xml_snippet, target="running").xml

def delete_pon_cos_profile_be(m, ont_id):
    profile_name = f"ont_{ont_id}_be"
    config = f"""
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <config xmlns="http://www.calix.com/ns/exa/base">
    <profile>
      <pon-cos-profile xmlns="http://www.calix.com/ns/exa/gpon-interface-base"
                       nc:operation="delete"
                       xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
        <name>{profile_name}</name>
      </pon-cos-profile>
    </profile>
  </config>
</config>
"""
    return m.edit_config(config=config, target="running").xml

def delete_pon_cos_profile_ef(m, ont_id):
    profile_name = f"ont_{ont_id}_ef"
    config = f"""
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <config xmlns="http://www.calix.com/ns/exa/base">
    <profile>
      <pon-cos-profile xmlns="http://www.calix.com/ns/exa/gpon-interface-base"
                       nc:operation="delete"
                       xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
        <name>{profile_name}</name>
      </pon-cos-profile>
    </profile>
  </config>
</config>
"""
    return m.edit_config(config=config, target="running").xml


def unassign_pon_cos_profile(m, ont_id):
    config = f"""
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <config xmlns="http://www.calix.com/ns/exa/base">
    <system>
      <ont xmlns="http://www.calix.com/ns/exa/gpon-interface-base">
        <ont-id>{ont_id}</ont-id>
        <pon-us-cos>
          <index>user-1</index>
        </pon-us-cos>
      </ont>
    </system>
  </config>
</config>
"""
    return m.edit_config(target="running", config=config).xml



def clear_interface_ont_ethernet(m, interface_name, svlan):
    config = f"""
<config>
  <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
    <interface>
      <name>{interface_name}</name>
      <ont-ethernet xmlns="http://www.calix.com/ns/exa/gpon-interface-std"
                    xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
        <role>uni</role>
        <l2cp-action>tunnel</l2cp-action>
        <vlan nc:operation="delete">
          <vlan-id>{svlan}</vlan-id>
        </vlan>
      </ont-ethernet>
    </interface>
  </interfaces>
</config>
"""
    return m.edit_config(config=config, target="running").xml


#######

def delete_class_map_from_interface(m, interface_name, class_map_name, policy_map_name, vlan_id):
    config = f"""
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
    <interface>
      <name>{interface_name}</name>
      <ont-ethernet xmlns="http://www.calix.com/ns/exa/gpon-interface-std">
        <vlan>
          <vlan-id>{vlan_id}</vlan-id>
          <policy-map>
            <name>{policy_map_name}</name>
            <class-map-ethernet nc:operation="delete"
                                 xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
              <name>{class_map_name}</name>
            </class-map-ethernet>
          </policy-map>
        </vlan>
      </ont-ethernet>
    </interface>
  </interfaces>
</config>
"""
    return m.edit_config(target="running", config=config).xml




def delete_policy_map_from_interface(m, interface_name, policy_map_name):
    config = f"""
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
    <interfaces>
      <interface>
        <name>{interface_name}</name>
        <ont-ethernet xmlns="http://www.calix.com/ns/exa/gpon-interface-std">
          <vlan>
            <policy-map nc:operation="delete"
                        xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
              <name>{policy_map_name}</name>
            </policy-map>
          </vlan>
        </ont-ethernet>
      </interface>
    </interfaces>
</config>
"""
    return m.edit_config(target="running", config=config).xml
def delete_vlan_from_interface(m, interface_name, vlan_id):
    config = f"""
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
    <interfaces>
      <interface>
        <name>{interface_name}</name>
        <ont-ethernet xmlns="http://www.calix.com/ns/exa/gpon-interface-std">
          <vlan nc:operation="delete"
                xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
            <vlan-id>{vlan_id}</vlan-id>
          </vlan>
        </ont-ethernet>
      </interface>
    </interfaces>
</config>
"""
    return m.edit_config(target="running", config=config).xml

def delete_policy_map_direct(m, policy_map_name):
    config = f"""
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <config xmlns="http://www.calix.com/ns/exa/base">
    <profile>
      <policy-map nc:operation="delete"
                  xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
        <name>{policy_map_name}</name>
      </policy-map>
    </profile>
  </config>
</config>
"""
    try:
        response = m.edit_config(target="running", config=config)
        print(f"✔️ Policy-map {policy_map_name} cancellata con successo")
        return response.xml
    except RPCError as rpc_err:
        print(f"❌ RPCError durante la cancellazione diretta della policy-map {policy_map_name}:")
        print(rpc_err)
        raise
    except Exception as exc:
        print(f"❌ Errore inatteso durante delete_policy_map_direct:")
        print(exc)
        raise



######



def delete_service(m, ont_id, ethernet_port, svlan, profile):
    replies = []

    # Calcola i nomi coerenti con la configurazione
    interface_name = f"{ont_id}/x1"
    class_map_name = f"Eth-match-any-{ont_id}"
    policy_map_name = f"ELINE_PM_{ont_id}"

    def log_and_run(label, func):
        try:
            print(f"→ Esecuzione: {label}")
            result = func()
            print(f"← Successo: {label}")
            return result
        except Exception as e:
            print(f"✖ Errore in {label}: {e}")
            raise RuntimeError(f"Errore durante '{label}': {str(e)}")

    # 1) Disattiva la porta Ethernet
    replies.append(log_and_run("deactivate_ethernet", lambda: deactivate_ethernet(m, ethernet_port)))

    # 2) Rimuove profilo CoS associato alla ONT
    replies.append(log_and_run("unassign_pon_cos_profile", lambda: unassign_pon_cos_profile(m, ont_id)))

    #replies.append(log_and_run("delete_policy_map_direct",    lambda: delete_policy_map_direct(m, policy_map_name)))

    # 3) Rimuove class-map dalla interfaccia
    #replies.append(log_and_run("delete_class_map_from_interface", lambda: delete_class_map_from_interface(m, interface_name, class_map_name, policy_map_name, svlan)))

    # 4) Rimuove policy-map dalla interfaccia
    #replies.append(log_and_run("delete_policy_map_from_interface", lambda: delete_policy_map_from_interface(m, interface_name, policy_map_name)))

    # 5) Rimuove VLAN dalla interfaccia
    #replies.append(log_and_run("delete_vlan_from_interface", lambda: delete_vlan_from_interface(m, interface_name, svlan)))

    # 6) Cancella policy-map globale (deve avvenire dopo la rimozione dalla interfaccia)
    #replies.append(log_and_run("delete_policy_map_eline", lambda: delete_policy_map_eline(m, ont_id)))

    # 7) Cancella class-map globale (dopo che non è più referenziata)
    #replies.append(log_and_run("delete_class_map_ethernet_match_any", lambda: delete_class_map_ethernet_match_any(m, ont_id)))

    # 8) Cancella profilo CoS
    '''
    if profile == "be":
        replies.append(log_and_run("delete_pon_cos_profile_be", lambda: delete_pon_cos_profile_be(m, ont_id)))
    elif profile == "ef":
        replies.append(log_and_run("delete_pon_cos_profile_ef", lambda: delete_pon_cos_profile_ef(m, ont_id)))
    else:
        raise ValueError("Valore 'profile' non valido (usa 'be' o 'ef')")
    '''

    # 9) Cancella ONT
    replies.append(log_and_run("delete_ont", lambda: delete_ont(m, ont_id)))

    ##TODO: aggiustare controllo sulla banda
    if ethernet_port == "1":
        deactivate_xp1()
    if ethernet_port == "2":
        deactivate_xp2()

    # Ritorno XML cumulativo
    root = etree.Element("rpc-replies")
    for r in replies:
        if r:
            try:
                parsed = etree.fromstring(strip_xml_decl(r))
                root.append(parsed)
            except Exception as e:
                error_elem = etree.SubElement(root, "error")
                error_elem.text = f"Invalid XML: {str(e)}"

    return etree.tostring(root, pretty_print=True).decode()









def get_topology(m):
    """
    Esegue un <get> con filtro subtree per recuperare la lista degli ONT scoperti
    sulle interfacce PON (Calix GPON).

    Parametri
    ---------
    m : ncclient.manager.Manager
        Sessione NETCONF già aperta verso l’OLT.
    """
    xml_filter = """
      <interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface>
          <pon xmlns="http://www.calix.com/ns/exa/gpon-interface-std">
            <discovered-onts/>
          </pon>
          <name/>
        </interface>
      </interfaces-state>
    """

    try:
        # Il primo argomento ('subtree', ...) dice a ncclient che il filtro è un subtree‑filter.
        reply = m.get(("subtree", xml_filter))
        # reply.data_xml ritorna l’XML come stringa (senza gli header rpc‑reply).
        print(reply.data_xml)
        return reply
    except RPCError as err:
        print(f"Errore RPC: {err}")
        raise
    except Exception as exc:
        print(f"Errore generico: {exc}")
        raise


def get_pon_cos_profiles(m):
    """
    Recupera tutti i profili PON-COS configurati sul dispositivo.

    Parametri:
    - m: sessione NETCONF ncclient.manager.Manager

    Ritorna:
    - Lista di dizionari, ciascuno contenente:
        - name
        - prio
        - bw_type (se presente)
        - bw_maximum (se presente)
        - bw_minimum (se presente)
        - cos_type (se presente)
    """
    xml_filter = '''
    <config xmlns="http://www.calix.com/ns/exa/base">
      <profile>
        <pon-cos-profile xmlns="http://www.calix.com/ns/exa/gpon-interface-base"/>
      </profile>
    </config>
    '''

    try:
        response = m.get(("subtree", xml_filter))
        root = etree.fromstring(response.xml.encode())

        ns = {
            "calixb": "http://www.calix.com/ns/exa/base",
            "gpon": "http://www.calix.com/ns/exa/gpon-interface-base"
        }

        profiles = []

        for profile in root.findall(".//gpon:pon-cos-profile", namespaces=ns):
            entry = {}

            name_elem = profile.find("gpon:name", namespaces=ns)
            prio_elem = profile.find("gpon:prio", namespaces=ns)
            bw_elem = profile.find("gpon:bw", namespaces=ns)
            cos_type_elem = profile.find("gpon:cos-type", namespaces=ns)

            entry["name"] = name_elem.text if name_elem is not None else None
            entry["prio"] = prio_elem.text if prio_elem is not None else None

            if bw_elem is not None:
                bw_type = bw_elem.find("gpon:type", namespaces=ns)
                bw_max = bw_elem.find("gpon:maximum", namespaces=ns)
                bw_min = bw_elem.find("gpon:minimum", namespaces=ns)

                entry["bw_type"] = bw_type.text if bw_type is not None else None
                entry["bw_maximum"] = bw_max.text if bw_max is not None else None
                entry["bw_minimum"] = bw_min.text if bw_min is not None else None
            else:
                entry["bw_type"] = entry["bw_maximum"] = entry["bw_minimum"] = None

            entry["cos_type"] = cos_type_elem.text if cos_type_elem is not None else None

            profiles.append(entry)

        return profiles

    except Exception as e:
        print(f"Errore durante il recupero dei PON COS profiles: {e}")
        return []

def get_total_bandwidth_allocated(m):
    """
    Recupera tutti i profili 'pon-us-cos-profile' assegnati agli ONT
    e calcola la somma totale di bw_minimum e bw_maximum dai relativi profili.

    Parametri:
    - m: sessione NETCONF ncclient.manager.Manager

    Ritorna:
    - Dizionario con:
        - total_bw_minimum (int)
        - total_bw_maximum (int)
    """
    xml_filter = '''
    <config xmlns="http://www.calix.com/ns/exa/base">
      <system>
        <ont xmlns="http://www.calix.com/ns/exa/gpon-interface-base">
        </ont>
      </system>
    </config>
    '''

    try:
        response = m.get(("subtree", xml_filter))
        root = etree.fromstring(response.xml.encode())

        ns = {
            "base": "http://www.calix.com/ns/exa/base",
            "gpon": "http://www.calix.com/ns/exa/gpon-interface-base"
        }

        # Estrai tutti i nomi dei profili usati
        profile_names = set()
        for node in root.findall(".//gpon:pon-us-cos-profile", namespaces=ns):
            if node.text:
                profile_names.add(node.text)

        # Recupera tutti i profili disponibili
        all_profiles = get_pon_cos_profiles(m)

        total_bw_min = 0
        total_bw_max = 0

        for name in profile_names:
            matching = [p for p in all_profiles if p["name"] == name]
            if matching:
                profile = matching[0]
                try:
                    if profile["bw_minimum"]:
                        total_bw_min += int(profile["bw_minimum"])
                    if profile["bw_maximum"]:
                        total_bw_max += int(profile["bw_maximum"])
                except ValueError:
                    print(f"Valori non numerici per il profilo {name}, ignorati.")
            else:
                print(f"Profilo {name} non trovato nella configurazione.")

        return {
            "total_bw_minimum": total_bw_min,
            "total_bw_maximum": total_bw_max
        }

    except Exception as e:
        print(f"Errore durante il calcolo della banda totale: {e}")
        return {
            "total_bw_minimum": 0,
            "total_bw_maximum": 0
        }

def check_bandwidth_and_switch_config(m, threshold_bps, mode="mcf"):
    """
    Controlla la banda totale allocata e lancia la configurazione appropriata.

    Parametri:
    - m: sessione NETCONF ncclient.manager.Manager già aperta
    - threshold_bps: soglia in bit per secondo
    - mode: 'mcf' o 'b2b' (default: 'mcf')

    Se la banda massima supera threshold_bps → configura 2x2_<mode>
    Altrimenti → configura 2x1_<mode>
    """
    try:
        totals = get_total_bandwidth_allocated(m)
        bw_max = totals["total_bw_maximum"]
        print(f"Totale banda massima allocata: {bw_max} bps")

        if bw_max > threshold_bps:
            print(f"Soglia superata. Avvio configurazione 2x2_{mode}.")
            subprocess.run(["python3", "configure_scenario.py", "-c", "2x2", "-m", mode])
        else:
            print(f"Soglia non superata. Avvio configurazione 2x1_{mode}.")
            subprocess.run(["python3", "configure_scenario.py", "-c", "2x1", "-m", mode])

    except Exception as e:
        print(f"Errore durante il controllo della banda e la configurazione: {e}")



def delete_ont(m, ont_id):
    """
    Cancella una ONT specifica identificata da ont_id.

    Parametri:
    - m: sessione NETCONF ncclient.manager.Manager
    - ont_id: ID numerico o stringa dell'ONT (es. 1, 2, "string")
    """

    xml_snippet = f"""
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <config xmlns="http://www.calix.com/ns/exa/base">
    <system>
      <ont xmlns="http://www.calix.com/ns/exa/gpon-interface-base"
           nc:operation="delete"
           xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
        <ont-id>{ont_id}</ont-id>
      </ont>
    </system>
  </config>
</config>
"""

    try:
        response = m.edit_config(target="running", config=xml_snippet)
        print(f"ONT {ont_id} cancellata.")
        print(response)
    except Exception as e:
        print(f"Errore durante la cancellazione della ONT {ont_id}: {e}")



def create_ont(m, ont_id, profile_id, serial_number):
    """
    Crea una ONT generica con i parametri specificati.

    Parametri:
    - m: sessione NETCONF ncclient.manager.Manager
    - ont_id: ID numerico o stringa dell'ONT (es. 1, 2, "string")
    - profile_id: ID del profilo (es. "801XGS")
    - serial_number: numero seriale dell'ONT (es. "47846E")
    """

    xml_snippet = f"""
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <config xmlns="http://www.calix.com/ns/exa/base">
    <system>
      <ont xmlns="http://www.calix.com/ns/exa/gpon-interface-base">
        <ont-id>{ont_id}</ont-id>
        <profile-id>{profile_id}</profile-id>
        <serial-number>{serial_number}</serial-number>
      </ont>
    </system>
  </config>
</config>
"""

    try:
        response = m.edit_config(target="running", config=xml_snippet)
        print(f"ONT {ont_id} creata.")
        print(response)
    except Exception as e:
        print(f"Errore durante la creazione della ONT {ont_id}: {e}")


def activate_xp2(host="10.30.7.6", username="sysadmin", password="sysadmin",
                   ):
    """
    Disattiva l’interfaccia PON 1/1/xp2 tramite SSH/CLI.

    Parametri opzionali:
        shutdown_cmd  – comando da eseguire nell’interfaccia
        host          – IP o FQDN dell’OLT
        username      – utente SSH
        password      – password SSH
    """
    try:
        # 1) Apertura sessione SSH
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=host, username=username, password=password, look_for_keys=False)

        # 2) Shell interattiva
        chan = client.invoke_shell()
        time.sleep(5)              # attesa prompt iniziale
        chan.recv(65535*10)

        # 3) Sequenza comandi
        for cmd in (
            "configure",
            "no interface pon 1/1/xp2 shutdown",
            "exit",                  # esce dal contesto interfaccia
            "exit"                   # esce da configuration-mode
        ):
            chan.send(cmd + "\n")
            time.sleep(1)          # piccola attesa dopo ogni invio

        # 4) Stampa dell’output ricevuto
        output = chan.recv(65535).decode(errors="ignore")
        #print(output)
        print("interface xp2 activated")

    except Exception as e:
        print(f"Errore durante l'attivazione di xp2: {e}")
    finally:
        try:
            client.close()
        except:
            pass

def activate_xp1(host="10.30.7.6", username="sysadmin", password="sysadmin",
                   ):
    """
    Disattiva l’interfaccia PON 1/1/xp2 tramite SSH/CLI.

    Parametri opzionali:
        shutdown_cmd  – comando da eseguire nell’interfaccia
        host          – IP o FQDN dell’OLT
        username      – utente SSH
        password      – password SSH
    """
    try:
        # 1) Apertura sessione SSH
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=host, username=username, password=password, look_for_keys=False)

        # 2) Shell interattiva
        chan = client.invoke_shell()
        time.sleep(5)              # attesa prompt iniziale
        chan.recv(65535*10)

        # 3) Sequenza comandi
        for cmd in (
            "configure",
            "no interface pon 1/1/xp1 shutdown",
            "exit",                  # esce dal contesto interfaccia
            "exit"                   # esce da configuration-mode
        ):
            chan.send(cmd + "\n")
            time.sleep(1)          # piccola attesa dopo ogni invio

        # 4) Stampa dell’output ricevuto
        output = chan.recv(65535).decode(errors="ignore")
        #print(output)
        print("interface xp1 activated")

    except Exception as e:
        print(f"Errore durante l'attivazione di xp1: {e}")
    finally:
        try:
            client.close()
        except:
            pass

def deactivate_xp2(host="10.30.7.6", username="sysadmin", password="sysadmin",
                   ):
    """
    Disattiva l’interfaccia PON 1/1/xp2 tramite SSH/CLI.

    Parametri opzionali:
        shutdown_cmd  – comando da eseguire nell’interfaccia
        host          – IP o FQDN dell’OLT
        username      – utente SSH
        password      – password SSH
    """
    try:
        # 1) Apertura sessione SSH
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=host, username=username, password=password, look_for_keys=False)

        # 2) Shell interattiva
        chan = client.invoke_shell()
        time.sleep(5)              # attesa prompt iniziale
        chan.recv(65535*10)

        # 3) Sequenza comandi
        # 3) Sequenza comandi
        for cmd in (
                "configure",
                "interface pon 1/1/xp2 shutdown",
                "exit",  # esce dal contesto interfaccia
                "exit"  # esce da configuration-mode
        ):
            chan.send(cmd + "\n")
            time.sleep(1)  # piccola attesa dopo ogni invio

        # 4) Stampa dell’output ricevuto
        output = chan.recv(65535*10).decode(errors="ignore")
        #print(output)
        print("interface xp2 deactivated")

    except Exception as e:
        print(f"Errore durante la disattivazione di xp2: {e}")
    finally:
        try:
            client.close()
        except:
            pass

def deactivate_xp1(host="10.30.7.6", username="sysadmin", password="sysadmin",
                   ):
    """
    Disattiva l’interfaccia PON 1/1/xp1 tramite SSH/CLI.

    Parametri opzionali:
        shutdown_cmd  – comando da eseguire nell’interfaccia
        host          – IP o FQDN dell’OLT
        username      – utente SSH
        password      – password SSH
    """
    try:
        # 1) Apertura sessione SSH
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=host, username=username, password=password, look_for_keys=False)

        # 2) Shell interattiva
        chan = client.invoke_shell()
        time.sleep(5)              # attesa prompt iniziale
        chan.recv(65535*10)

        # 3) Sequenza comandi
        # 3) Sequenza comandi
        for cmd in (
                "configure",
                "interface pon 1/1/xp1 shutdown",
                "exit",  # esce dal contesto interfaccia
                "exit"  # esce da configuration-mode
        ):
            chan.send(cmd + "\n")
            time.sleep(1)  # piccola attesa dopo ogni invio

        # 4) Stampa dell’output ricevuto
        output = chan.recv(65535*10).decode(errors="ignore")
        #print(output)
        print("interface xp1 deactivated")

    except Exception as e:
        print(f"Errore durante la disattivazione di xp1: {e}")
    finally:
        try:
            client.close()
        except:
            pass



# Funzione principale per eseguire le operazioni in sequenza
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
            # Eseguire in sequenza le operazioni
            #delete_ont2(m)
            #create_ont2(m)
            #create_ont_eth_2x1(m)
            #create_vlan(m, 333)
            #add_vlan_to_general_tsp(m,456)
            #create_class_map_ethernet_match_any(m,3)
            #create_policy_map_eline(m,2)
            #create_pon_cos_profile_be(m,2)
            #create_pon_cos_profile_ef(m, 2,2000000)
            #create_interface_ont_ethernet(m,2,1,333)
            #apply_pon_cos_profile_be(m,1)
            #apply_pon_cos_profile_ef(m, 1)
            #activate_ethernet(m,2)
            ##create_service(m, 1, 23, 2, 333, "ef", bw=2500000)
            #get_topology(m)
            #check_bandwidth_and_switch_config(m,2600000 )
            #delete_ont(m, 1)
            #delete_ont(m, 2)
            #create_ont(m, ont_id=1, profile_id="801XGS", serial_number="47846E")
            #create_ont(m, ont_id=2, profile_id="801XGS", serial_number="478490")
            #activate_xp2(host,username,password)
            #create_ont(m, 1, profile_id="801XGS", serial_number="47846E")
            #create_ont(m, 2, profile_id="801XGS", serial_number="478490")
            activate_xp1()
            #activate_xp2()
            #deactivate_xp1()




    except Exception as e:
        print(f"Errore durante la connessione al dispositivo: {e}")

# Esecuzione dello script
if __name__ == '__main__':
    main()
