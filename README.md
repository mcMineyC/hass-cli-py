# hass-cli

A Home Assitant CLI written in Python

## NOTE: Credentials are stored in config.json.  Copy or rename config_template.json to config.json and populate required fields before running.

### Building
On Linux/macOS:

`pip3 install -r requirements.txt`

`nuitka3 --follow-imports cli.py -o hass-cli`

On Windows:

`python3 -m pip install -r requirements.txt`

`python3 -m nuitka --follow-imports cli.py -o hass-cli.exe`