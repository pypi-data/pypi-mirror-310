[![CC BY-NC 4.0][cc-by-nc-shield]][cc-by-nc][![Actions CI](https://github.com/NetworkRADIUS/rs232-to-pdu/actions/workflows/python-app.yml/badge.svg)](https://github.com/NetworkRADIUS/rs232-to-pdu/actions/workflows/python-app.yml)

## RS-232 to PDU Tool

The RS-232 to PDU tool allows admins to send byte strings through an RS-232 connector to control a SNMP-enabled 
PDU. Supported operations are to turn a specific outlet port ON, OFF, and CYCLE.

---

## Supported Serial Commands

- Turn outlet on: ```on <bank> <port>```
- Turn outlet off: ```of <bank> <port>```
- Cycle (restart) outlet: ```cy <bank> <port>```

```<bank>``` and ```<port>``` must be between (0-255).

---

## Health Check

Health checks will send a ```GET``` command to the SNMP agent. 

If a response is successfully received, the health check is considered to have passed. If the command 
timed-out or returned an error, the health check is considered to have failed. At this point, the tool will log this 
event, but continue with other operations.

Health checks will have priority over other commands, i.e. if there is a pending health check, it will be executed
before any other SNMP operations.

Healthcheck frequency are configurable in the `config.yaml` file, under `healthcheck.frequency`.

---

## Power States

Maps serial commands, `on`, `of` and optionally `cy` (cycle) to SNMP values set on the OIDs that control outlet states.
If `cy` is not specified, and a `cy` command is received, the outlet state is set to `of`, followed by a delay of
`power_states.cy_delay` seconds, then `of`.

---

## SNMP Command Buffering
To prevent the SNMP agent from being overwhelmed by operations, this tool will not send a command to the SNMP agent until 
a response for the previous operation has been received. As such, all queued operations will be stored in a priority based
FIFO queue.  SNMP operations resulting from serial commands will be processed in the order that they are received, with
automatic health checks taking priority and being inserted at the front of the queue.

---

## SNMP Authentication

This tool supports v1, v2, and v3 SNMP authentication.

The authentication version for each bank should be listed in the `config.yaml` file. Only a single SNMP version is allowed for each bank.

When using SNMP v3, the user may also choose what security level they desire. The accepted values are ```noAuthNoPriv```
, ```authNoPriv```, and ```authPriv```.

- ```noAuthNoPriv```: SNMP request will be sent without any credentials aside from username (no authentication or confidentiality)
- ```authNoPriv```: SNMP request will be sent with a username and authorization passphrase (authentication but no confidentiality)
- ```authPriv```: SNMP request will be sent with username, authorization and privacy passphrase (authentication and confidentiality)

---

## Logging

This tools supports the option of configuring logging output to a file, syslog, or stream. Only one destination may be specified. 
The destination should be placed under `log.file`, `log.syslog`, or `log.stream`. For file and stream outputs, a single string is 
expected as the destination. For syslog, a `facility` field is required.

If no logging configuration is present, the tool will default to stdout as the destination.

Below are sample configurations.

```yaml
# config.yaml

# Sample 1 : logging to file
log:
  file: destination.log

# Sample 2 : logging to syslog based on facility
log:
  syslog:
    facility: user

# Sample 3: logging to stream
log:
  stream: stdout
```

---

## Device Templates

Outlet definitions (e.g. SNMP OIDs) can be placed into a template that can be shared across multiple devices. 

Templates can either go in the `<transport>.devices.custom.<name>` section in `config.yaml`, or be placed in a separate file named `<name>.yaml` located at the filepath described by `<transport>.devices.path`.

To use a template, the `devices.<name>.device` field must contain the name of the template.

All device names must conform to the BNF grammar of:

```bnf
<name> ::= <string> (("-" | "_") <name>)*
<string> ::= ([A-Z] | [a-z] | [0-9])+
```

Below are sample configurations.

Sample 1: templates stored in `config.yaml`
```yaml
# config.yaml
snmp:
  devices:
    custom:
      foo:
        outlets:
          '001': '1.3.6.1'
        power_states:
          'on': 1

devices:
  '001':
    device: foo
```

Sample 2: external template
```yaml
# config.yaml
snmp:
  devices:
    path: './devices/'

devices:
  '001':
    device: foo
  
# ./devices/foo.yaml
outlets:
  '001': '1.3.6.1'
  '002': '1.3.6.2'
power_states:
  'on': 1
```

---

## Contributing to device templates

To create a new device template, create a yaml file under a directory in `src/rs232_to_pdu/devices/`. As a general rule, the template file should be named after the device product number, while the directory the template is in should help describe the template (i.e., manufacturer).

---

## Config Format

This tool expects a configuration file called ```config.yaml```, placed under ```/etc/rs232_to_pdu/```. This file must 
conform the yaml format and have the following sections.

* ```log```:
    * ```file``` | ```stream```: logging destination as a string
    * ```syslog```:
      * ```facility```: facility name for syslogs

* ```serial```:
  * ```device```: string value of serial port tty file
  * ```timeout```: time in seconds before timing out serial connection

* ```healthcheck```:
  * ```frequency```: time in seconds in between healthchecks

* ```snmp```:
  * ```retry```:
    * ```max_attempts```: integer value of maximum attempts allowed for an SNMP command
    * ```delay```: time in seconds to wait between SNMP command retries
    * ```timeout```: time in seconds before timing out SNMP commands
  * ```devices```:
    * ```custom```:
      * ```<device name>```
        * ```outlets```:
          * ```<port numbers*>```: string value of OID for this port
        * ```power_states```:
          * ```<power_state>```: value for this power state
* ```path```: path to template files

* ```banks```:
  * ```<bank number>*```
    * ```snmp```:
      * ```v1``` | ```v2```:
        * ```public_community```: string value of public community name
        * ```private_community```: string value of private community name
      * ```v3```:
        * ```user```: string value of SNMP username
        * ```auth_protocol```: string value of authentication protocol
        * ```auth_passphrase```: string value of authentication passphrase
        * ```priv_protocol```: string value of privacy protocol
        * ```priv_passphrase```: string value of privacy passphrase
        * ```security_level```: ```noAuthNoPriv``` | ```authNoPriv``` | ```authPriv```
      * ```ip_address```: string value of IP address of SNMP agent
      * ```port```: integer value of network port of SNMP agent
      * ```device```:
        * ```outlets```:
          * ```<port number>*```: string value of OID for this port\
        * ```power_states```:
          * ```'on'```: value for on state
          * ```'of'```: value for on state
          * ```'cy'```: value for on state

### Sample Config

```
log:
  file: {{ log_destination }}

serial:
  device: {{ device }}
  timeout: 0

healthcheck:
  frequency: 5

power_states:
  cy_delay: 5

snmp:
  retry:
    max_attempts: 3
    delay: 5
    timeout: 5
  devices:
    custom:
      bar:
        outlets:
          '001': '1.3.6.1'
        power_states:
          'on': 1
          'of': 2
    path: './etc/'

devices:
  '001':
    snmp:
      v1:
        public_community: {{ public_community_name }}
        private_community: {{ private_community_name }}
      ip_address: {{ ip_address }}
      port: {{ port }}
    device:
      outlets:
        '001': {{ oid }}
        '002': {{ oid }}
      power_states:
        on: 1
        of: 2
        cy: 3
  '002':
    snmp:
      v2:
        public_community: {{ public_community_name }}
        private_community: {{ private_community_name }}
      ip_address: {{ ip_address }}
      port: {{ port }}
    device: foo
  '003':
    snmp:
      v3:
        user: {{ snmp_user }}
        auth_protocol: {{ snmp_auth }}
        auth_passphrase: '{{ snmp_auth_passphrase }}'
        priv_protocol: {{ snmp_priv }}
        priv_passphrase: '{{ snmp_priv_passphrase }}'
        security_level: {{ snmp_security_level }}
      ip_address: {{ ip_address }}
      port: {{ port }}
    device: bar
```

## License
This work is licensed under a
[Creative Commons Attribution-NonCommercial 4.0 International License][cc-by-nc].

[![CC BY-NC 4.0][cc-by-nc-image]][cc-by-nc]

[cc-by-nc]: https://creativecommons.org/licenses/by-nc/4.0/
[cc-by-nc-image]: https://licensebuttons.net/l/by-nc/4.0/88x31.png
[cc-by-nc-shield]: https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg
