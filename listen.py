import socket, os, json, time
from websockets.sync.client import connect
from common import config_data, auth_header, log
import asyncio
async def main(id):
    uri = config_data["url"].replace("https://", "wss://").replace("http://", "ws://")
    print("Connecting to websocket at "+uri)
    async with connect(uri+"/api/websocket") as ws:
        print("Authenticating...")
        log(ws.recv())
        ws.send(json.dumps(auth_header))
        time.sleep(1)
        log(await ws.recv())
        id = 1
        ws.send(json.dumps({
            "id": id,
            "type": "subscribe_events",
            "event_type": "state_changed"
        }))
        log(await ws.recv())
        id += 1
        while True:
            message = json.loads(await ws.recv())
            if message["type"] == "event":
                if message["event"]["data"]["entity_id"] == id:
                    state = message["event"]["data"]["new_state"]
                    print(state)

#       Start websocket
def changed(id):
    try:
        asyncio.run(main(id))
    except Exception:
        print("Error")
