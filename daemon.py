import socket, os, json, time
from websockets.sync.client import connect
from common import config_data, auth_header, log
# Set the path for the Unix socket
socket_path = '/tmp/hass_daemon.sock'

# remove the socket file if it already exists
try:
    os.unlink(socket_path)
except OSError:
    if os.path.exists(socket_path):
        raise

# Create the Unix socket server
print("Creating Unix socket")
server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

# Bind the socket to the path
server.bind(socket_path)

# Listen for incoming connections
server.listen(2)
uri = config_data["url"].replace("https://", "wss://").replace("http://", "ws://")
print("Connecting to websocket")
with connect(uri+"/api/websocket") as ws:
    print("Authenticating...")
    log(ws.recv())
    ws.send(json.dumps(auth_header))
    time.sleep(1)
    log(ws.recv())
    id = 1
    while True:
        print('Listening for Unix connections...')
        connection, client_address = server.accept()

        try:
            print('Connection from ', str(connection).split(", ")[0][-4:])

            # receive data from the client
            while True:
                data = connection.recv(1024000)
                if not data:
                    break
                m = data.decode()
                print("Got data: "+m)
                m = json.loads(m)
                m["id"] = id
                print("Sending data: "+json.dumps(m))
                ws.send(json.dumps(m))
                id += 1
                # Send a response back to the client
                response = ws.recv()
                print("Got response of length: "+str(len(response)))
                connection.sendall(response.encode())
        finally:
            # close the connection
            connection.close()