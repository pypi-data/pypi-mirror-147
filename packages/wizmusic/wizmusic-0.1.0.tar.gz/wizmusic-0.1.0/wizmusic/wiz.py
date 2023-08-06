import sys
import json
import socket
from collections import deque


class Wiz:
    STATE_FIELDS = ("r", "g", "b", "c", "w", "dimming", "temp")

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._states = deque()

    def __enter__(self):
        self.push_state()
        return self

    def __exit__(self, *args, **kwargs):
        print("Restoring WiZ state...")
        self.pop_state()

    def _send(self, payload: dict) -> dict:
        body = json.dumps(payload)
        addr = (self.host, self.port)

        self.socket.sendto(body.encode("utf8"), addr)
        resp_content, resp_addr = self.socket.recvfrom(4096)

        if not resp_content or addr != resp_addr:
            print(f"{addr=} != {resp_addr} - {resp_content=}", file=sys.stderr)
            return {}

        return json.loads(resp_content)

    def get_state(self) -> dict:
        return self._send({"method": "getPilot"}).get("result")

    def on(self):
        return self._send({"method": "setPilot", "params": {"state": True}})

    def off(self):
        return self._send({"method": "setPilot", "params": {"state": False}})

    def set_color(self, rgb):
        r, g, b = rgb
        return self._send({"method": "setPilot", "params": {"r": r, "g": g, "b": b}})

    def push_state(self):
        """push state to the queue"""
        state = self.get_state()
        self._states.append(state)

    def pop_state(self):
        try:
            state = self._states.pop()
        except IndexError:
            return
        return self._send({
            "method": "setPilot",
            "params": {k: v for k, v in state.items() if k in self.STATE_FIELDS}
        })
