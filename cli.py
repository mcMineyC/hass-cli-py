import argparse
import light
parser = argparse.ArgumentParser(
                    prog='hass-cli',
                    description='A CLI for Home Assistant',
                    epilog='')
parser.add_argument('-sj', '--state-json', type=str,
                    help='state (in JSON format) to send to Home Assistant')
parser.add_argument('-s', '--state', type=str,
                    help='state to send to Home Assistant')
parser.add_argument('-i', '--id', type=str,
                    help='entity id to control')
parser.add_argument('-t', '--type', type=str,
                    help='type of entity')
args = parser.parse_args()
if (not args.type) or (not args.id) or (not args.state):
    parser.print_help()
    exit(0)

match args.type:
    case "light":
        if (not ((args.state == "on") or (args.state == "off"))):
            parser.print_help()
            print("state must be 'on' or 'off' for type 'light'")
            exit(0)
        light.light(args.id, args.state)