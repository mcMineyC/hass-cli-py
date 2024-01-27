import socket, os, json, time, asyncio
from websockets import connect
from common import config_data, auth_header, log
import light

async def main(ent_id):
    uri = config_data["url"].replace("https://", "wss://").replace("http://", "ws://")
    print("Connecting to websocket at "+uri)
    async with connect(uri+"/api/websocket") as ws:
        print("Authenticating...")
        log(await ws.recv())
        await ws.send(json.dumps(auth_header))
        log(await ws.recv())
        print("Subscribing to events")
        id = 1
        await ws.send(json.dumps({
            "id": id,
            "type": "subscribe_events",
            "event_type": "state_changed"
        }))
        log(await ws.recv())
        id += 1
        print("Waiting for changes...")
        while True:
            message = json.loads(await ws.recv())
            if message["type"] == "event":
                print("New event from entity: "+message["event"]["data"]["entity_id"])
                if message["event"]["data"]["entity_id"] == ent_id:
                    state = message["event"]["data"]["new_state"]
                    print(light.parseState(state))

#       Start websocket
def changed(entity_id):
    try:
        try:
            asyncio.run(main(entity_id))
        except KeyboardInterrupt:
            print("\nExiting...")
    except Exception as e:
        print("Error: "+str(e))
