import requests
from common import config_data
def light(name, state):
	data = {"entity_id": "light."+name}
	r = requests.post(url=(config_data["url"]+"/api/services/light/turn_"+state), json=data, headers=config_data["headers"])
	print(r.json())
