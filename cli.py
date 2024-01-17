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
parser.add_argument('-g', '--get', action='store_true',
                    help='get state of entity')
args = parser.parse_args()
if (not args.id):
    parser.print_help()
    exit(0)

match args.type:
    case "light":
        light.checkargs(parser)
        if args.state_json:
            light.lightjson(args.id, args.state_json)
        elif args.get:
            light.get(args.id)
        else:
            light.light(args.id, args.state)