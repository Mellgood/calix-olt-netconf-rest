topology_data = {
    "ietf-network:networks": {
      "network": [
        {
          "network-id": "PON:L2",
          "network-types": {
            "ietf-l2-topology:l2-topology": {}
          },
          "node": [
            {
              "node-id": "OLT",
              "ietf-network-topology:termination-point": [
                {
                  "tp-id": "xp1",
                  "ietf-l2-topology:l2-termination-point-attributes": {
                    "mac-address": "cc:be:59:4d:8b:80",
                    "encapsulation-type": "ietf-l2-topology:ethernet"
                  }
                }
              ]
            },
            {
              "node-id": "ONT 1",
              "ietf-network-topology:termination-point": [
                {
                  "tp-id": "1/x1",
                  "ietf-l2-topology:l2-termination-point-attributes": {
                    "mac-address": "cc:be:59:51:b3:e5",
                    "encapsulation-type": "ietf-l2-topology:ethernet"
                  }
                }
              ]
            },
            {
              "node-id": "ONT 2",
              "ietf-network-topology:termination-point": [
                {
                  "tp-id": "",
                  "ietf-l2-topology:l2-termination-point-attributes": {
                    "mac-address": "",
                    "encapsulation-type": "ietf-l2-topology:ethernet"
                  }
                }
              ]
            }
          ]
        }
      ]
    }
}
