import argparse
import light
import listen
parser = argparse.ArgumentParser(
                    prog='hass-cli',
                    description='A CLI for Home Assistant',
                    epilog='')
parser.add_argument('-i', '--id', type=str,
                    help='entity id to control')
sp = parser.add_subparsers(dest="type")
sp.required = True

lp = sp.add_parser("light")
lpa = lp.add_subparsers(dest="action")
lpa.required = True

lpas = lpa.add_parser("get")

lpas = lpa.add_parser("set")
lpas.add_argument('state', choices=["on", "off"], nargs="?")
lpas.add_argument('-r', "--raw", type=str, default=None)
lpas.add_argument('brightness', default=None, nargs="?")




listenp = sp.add_parser("listen")




args = parser.parse_args()
if (not args.id):
    parser.print_help()
    print("Missing entity id")
    exit(0)

match args.type:
    case "light":
        match args.action:
            case "set":
                if args.brightness is not None:
                    light.brightness(args.id, args.brightness)
                else:
                    if args.raw is not None:
                        light.raw(args.id, args.raw)
                    else:
                        light.light(args.id, args.state)
            case "get":
                light.get(args.id)
    case "listen":
        listen.changed(args.id)