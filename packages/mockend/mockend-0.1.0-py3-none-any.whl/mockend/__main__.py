import argparse
import json
from flask import Flask, abort, Response, request

app = Flask(__name__)
all_methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS', 'HEAD', 'TRACE']


def validate_path(configuration):
    """
    Args:
        configuration(dict): config dict
    Returns:
        (dict|none): returns config if path is valid, None otherwise

    """
    subpaths = list(filter(''.__ne__, request.path.split('/')))

    for sub_path in subpaths:
        if sub_path in configuration.keys():
            configuration = configuration.get(sub_path)
        else:
            return None

    return configuration


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=all_methods)
def mockend_service(path):
    """
    Args:
        path(str): incoming request path
    Returns:
        (Response): returns flask response
    """
    path_config = validate_path(config)

    if path_config:
        if request.method.lower() in path_config:
            path_config = path_config.get(request.method.lower())
            response_body = path_config.get('response')
            return Response(
                response=json.dumps(response_body) if type(response_body) in (dict, list) else response_body,
                status=path_config.get("status"),
                headers=path_config.get("headers"),
                mimetype=path_config.get("mimetype"),
                content_type=path_config.get("content_type"),
                direct_passthrough=path_config.get("direct_passthrough"),
            )
        else:
            abort(405)
    else:
        abort(404)


parser = argparse.ArgumentParser(prog='PROG', description='Model builder according to a given configuration.')
parser.add_argument('-c', '--config', metavar='', type=str, required=True, default='config.json', help='Path to the configuration file.')
parser.add_argument('-i', '--host', metavar='', type=str, required=False, default='localhost', help='Host address')
parser.add_argument('-p', '--port', metavar='', type=int, required=False, default=5555, help='Port number')
parser.add_argument('-d', '--debug', metavar='', type=bool, required=False, default=True, help='Debug mode')
args = parser.parse_args()

config = json.load(open(args.config))
app.run(host=args.host, port=args.port, debug=args.debug)
