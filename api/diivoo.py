import time

import tinytuya


class Diivoo:
    def __init__(
        self,
        gw_id: str,
        gw_address: str,
        id: str,
        node_id: str,
        local_key: str,
        zones: dict[str, int],
        version: float = 3.4,
        debug=False,
    ):
        self.gw = tinytuya.Device(
            gw_id,
            address=gw_address,
            local_key=local_key,
            persist=True,
            version=version,
        )

        # configure one or more children.  Every dev_id must be unique!
        #   cid is the "node_id" from devices.json
        #   node_id can be used as an alias for cid
        self.device = tinytuya.OutletDevice(id, node_id=node_id, parent=self.gw)
        self.zones: dict[str, bool] = dict.fromkeys(zones, False)
        self.zones_id: dict[int, str] = {val: key for (key, val) in zones.items()}
        self.zones_map: dict[str, int] = zones
        if debug:
            tinytuya.set_debug(True)

    def get(self) -> dict:
        POLL_TIME_RE = 60

        zones_rcv: dict[str, bool] = dict.fromkeys(self.zones, True)

        self.device.status(nowait=True)

        # See if any data is available
        polltime_re = time.time() + POLL_TIME_RE
        while all(zones_rcv.values()):
            data = self.device.receive()
            if data and "dps" in data:
                for key in self.zones_id.keys():
                    if str(key) in data["dps"]:
                        self.zones[self.zones_id[key]] = data["dps"][str(key)]
                        zones_rcv[self.zones_id[key]] = False

            if polltime_re <= time.time():
                polltime_re = time.time() + POLL_TIME_RE
                print(" > Resend Request for Status < ")
                self.device.status(nowait=True)

        return self.zones

    def activate(self, zone: str) -> None:
        self.device.set_status(on=True, switch=self.zones_map[zone])

    def deactivate(self, zone: str) -> None:
        self.device.set_status(on=False, switch=self.zones_map[zone])

    def set_status(self, on: bool, zone: str) -> None:
        self.device.set_status(on=on, switch=self.zones_map[zone])
