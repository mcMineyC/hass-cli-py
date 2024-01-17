import requests
from common import config_data
def light(name, state):
	data = {"entity_id": "light."+name}
	r = requests.post(url=(config_data["url"]+"/api/services/light/turn_"+state), json=data, headers=config_data["headers"])
	print(r.json())
def lightjson(name, data):
	r = requests.post(url=(config_data["url"]+"/api/states/light."+name), json=data, headers=config_data["headers"])
	print(r.json())
def get(name):
	r = requests.get(url=(config_data["url"]+"/api/states/light."+name), headers=config_data["headers"])
	o = r.json()
	if o["attributes"]["supported_color_modes"][0] == "brightness":
		bri = int(o["attributes"]["brightness"]) * (100) / (255);
		out = {
			"type": "monochrome",
			"state": o["state"],
			"brightness": round(bri)
		}
		print(out)
	else:
		print(o)
def checkargs(parser):
	args = parser.parse_args()
	if args.get:
		return
	elif (not ((args.state == "on") or (args.state == "off") or args.state_json)):
		parser.print_help()
		print("state must be 'on' or 'off', or JSON for type 'light'")
		exit(0)