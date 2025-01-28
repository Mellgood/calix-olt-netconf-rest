from ncclient import manager

# Dati di connessione al dispositivo
host = "10.10.10.30"  # Sostituisci con l'indirizzo IP del tuo dispositivo
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
        <pon-us-cos>
          <index>user-1</index>
          <pon-us-cos-profile>ont1_be</pon-us-cos-profile>
        </pon-us-cos>
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
        <pon-us-cos>
          <index>user-1</index>
          <pon-us-cos-profile>ont2_be</pon-us-cos-profile>
        </pon-us-cos>
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
              <name>Eth-math-any-2</name>
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
            <name>ELINE_PM_1</name>
            <class-map-ethernet>
              <name>Eth-math-any-1</name>
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
        <tsp-name>GENERAL_TSP</tsp-name>
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

def activate_ethernet(m, port_number):
    # Costruiamo l'XML che replichi la struttura di Netconf Explorer
    xml_snippet = f"""
<config>
  <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
    <interface>
      <name>1/1/x{port_number}</name>
      <ethernet xmlns="http://www.calix.com/ns/ethernet-std">
        <role>inni</role>
        <native-vlan>999</native-vlan>
        <transport-service-profile>GENERAL_TSP</transport-service-profile>
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
    # 1) Creazione VLAN (se necessario) - usiamo la S-VLAN
    create_vlan(m, svlan)

    # 2) Aggiunta VLAN al "general_tsp" (o a un TSP specifico)
    add_vlan_to_general_tsp(m, svlan)

    # 7) Attivazione della porta Ethernet
    activate_ethernet(m, ethernet_port)

    # 3) Creazione class-map Ethernet "match-any" per la ONT
    create_class_map_ethernet_match_any(m, ont_id)

    # 4) Creazione policy-map ELINE
    create_policy_map_eline(m, ont_id)

    # 5) Creazione e configurazione dell'interfaccia ONT Ethernet
    create_interface_ont_ethernet(m, ont_id, 1, svlan)

    # 6) In base al profilo richiesto, crea e applica i cos-profile
    if profile == "bw":
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
        raise ValueError("Valore di 'profile' non riconosciuto. Usa 'bw' o 'ef'.")


