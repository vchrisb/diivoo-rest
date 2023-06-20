# diivoo-rest

A simple RESTful API for a DIIVOO Irrigation.
Uses [Tinytuy](https://github.com/jasonacox/tinytuya) to interface it locally.

Requires the following environment variables:

```
TUYA_GW_ID="XXXXXX"
TUYA_GW_ADDRESS="192.168.1.X"
TUYA_DIIVOO_ID="XXXXXX"
TUYA_DIIVOO_NODE_ID="XXXXXX"
TUYA_LOCAL_KEY='XXXXXX'
TUYA_ZONES='{"zone1": 105, "zone2": 104}'
TUYA_ADMIN_PASSWORD="admin"
TUYA_DEBUG="False"
```
