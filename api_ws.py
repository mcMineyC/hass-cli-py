import os, socket, json


def service(domain, name, target = None, data = None):
    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    client.connect("/tmp/hass_daemon.sock")
    message = {
        "type": "call_service",
        "domain": domain,
        "service": name,
    }
    if target is not None:
        message["target"] = {'entity_id': target}
    if data is not None:
        message["service_data"] = data
    client.sendall(json.dumps(message).encode())
    resp = json.loads(client.recv(1024000).decode())
    if resp["success"] == False:
        print(resp["error"]["message"])
    else:
        print(200)
    client.close()
def state(entity_id):
    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    client.connect("/tmp/hass_daemon.sock")
    message = {
        "type": "get_states"
    }
    client.sendall(json.dumps(message).encode())
    resp = client.recv(1024000).decode()
    states = json.loads(resp)
    if states["success"] == True:
        for state in states["result"]:
            if state["entity_id"] == entity_id:
                return state
    client.close()