import api_ws as api
from common import config_data
import json
def light(name, state):
	api.service("light", "turn_"+state, target=name)

def brightness(name, bri):
	brii = int(bri) * (255) / (100); #Map brightness to 0-255 from 0-100
	api.service("light", "turn_on", target=name, data={"brightness": brii})

def raw(name, state):
	api.service("light", "turn_on", target=name, data=json.loads(state))

def get(name):
	o = api.state(name)
	if (o["attributes"]["supported_color_modes"][0] == "brightness" and len(o["attributes"]["supported_color_modes"]) == 1):
		if (o["attributes"]["brightness"] == None):
			bri = 0
		else:
			bri = int(o["attributes"]["brightness"]) * (100) / (255);
		out = {
			"type": "monochrome",
			"state": o["state"],
			"brightness": round(bri)
		}
		print(out)
	elif ("hs" in o["attributes"]["supported_color_modes"]):
		if ("color_temp" in o["attributes"]["supported_color_modes"]):
			if (o["attributes"]["brightness"] == None):
				bri = 0
			else:
				bri = round(int(o["attributes"]["brightness"]) * (100) / (255))
			
			if o["attributes"]["color_mode"] == "color_temp":
				out = {
					"type": "colork",
					"mode": "temp",
					"state": o["state"],
					"brightness": bri,
					"temp": o["attributes"]["color_temp"]
				}
				print(out)
			elif o["attributes"]["color_mode"] == "hs":
				out = {
					"type": "colork",
					"mode": "hs",
					"state": o["state"],
					"brightness": bri,
					"rgb": o["attributes"]["rgb_color"]
				}
				print(out)
			else:
				out = {
					"type": "colork",
					"state": "off",
					"brightness": 0,
				}
				print(out)
		else:
			out = {
				"type": "color",
				"mode": "hs",
				"state": o["state"],
				"brightness": bri,
				"rgb": o["attributes"]["rgb_color"]
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