# Calix E7-2 Network API - SEASON L'Aquila

This project exposes a RESTful API to manage network configurations on a Calix E7-2 Optical Line Terminal (OLT) via NETCONF. It is developed in the context of the SEASON project in L'Aquila and aims to simplify service creation, monitoring, and profile management for ONT devices.

## Features

- RESTful API built with Flask and Flask-RESTx
- NETCONF interaction via `ncclient`
- Full ONT service provisioning (VLAN, TSP, CoS Profiles)
- Hardware inventory parsing
- Development mode (no device interaction)

## Requirements

- Python 3.9+
- Calix E7-2 device reachable via NETCONF on port 830
- Docker (for containerized deployment)

## Usage

### Running Locally (for development)

Install Python dependencies:

```bash
pip install -r requirements.txt
```

Run in **development mode** (no connection to OLT):

```bash
export DEV=true
python main.py
```

Run in **production mode**:

```bash
unset DEV
python main.py
```

By default, the API server will be available at:  
`http://localhost:3333/`

---

### Running with Docker

Build the Docker image with a version tag:

```bash
docker build -t mellgood/season-laquila:1.0 .
```

Run the container:

```bash
docker run -p 3333:3333 --env DEV=true mellgood/season-laquila:1.0
```

To run in production mode (interacting with the OLT):

```bash
docker run -p 3333:3333 mellgood/season-laquila:1.0
```

Replace `:1.0` with your desired version tag (`:1.1`, `:2.0`, etc.).

---

## REST API Overview

| Endpoint                         | Method | Description                                 |
|----------------------------------|--------|---------------------------------------------|
| `/api/inventory`                | GET    | Retrieve ONT/OLT inventory from the device  |
| `/api/service`                  | POST   | Provision a new service on a given ONT      |
| `/api/pon-cos-profile/<name>`  | GET/PUT| Get or update PON CoS profiles              |
| `/api/running-config`           | GET    | Download current running config (XML)       |

---

## Directory Structure

```
.
├── main.py
├── model/
│   ├── netconf/            # NETCONF logic and service generation
│   ├── xml/                # XML parsing utilities
│   └── api_model/          # OpenAPI model definitions
├── api/
│   └── netconf/            # REST API namespaces
├── Dockerfile              # (to be added if not present)
└── running-config.xml      # Used in DEV mode only
```

---

## Notes

- Device-specific: this application is tailored for Calix E7-2 systems using their proprietary YANG modules.
- Use the `DEV=true` environment variable to develop and test without accessing the physical device.