import json
import os

from diivoo import Diivoo
from flask import Flask, request
from flask_httpauth import HTTPBasicAuth
from flask_restful import Api, Resource
from webargs.flaskparser import abort, parser
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
api = Api(app)
auth = HTTPBasicAuth()
app.config["RESTFUL_JSON"] = {"sort_keys": True}
debug = False

try:
    GW_ID = os.environ["TUYA_GW_ID"]
    GW_ADDRESS = os.environ["TUYA_GW_ADDRESS"]
    ID = os.environ["TUYA_DIIVOO_ID"]
    NODE_ID = os.environ["TUYA_DIIVOO_NODE_ID"]
    LOCAL_KEY = os.environ["TUYA_LOCAL_KEY"]
    ADMIN_PASSWORD = os.environ["TUYA_ADMIN_PASSWORD"]
    ZONES = os.getenv("TUYA_ZONES")
except KeyError:
    raise Exception(
        "Environmental Variables TUYA_GW_ID, TUYA_GW_ADDRESS, TUYA_DIIVOO_ID TUYA_DIIVOO_NODE_ID TUYA_LOCAL_KEY TUYA_ADMIN_PASSWORD and TUYA_ZONES need to be present!"
    )

if os.getenv("TUYA_DEBUG", "") == "True":
    debug = True

users = {"admin": generate_password_hash(ADMIN_PASSWORD)}

diivoo = Diivoo(
    gw_id=GW_ID,
    gw_address=GW_ADDRESS,
    id=ID,
    node_id=NODE_ID,
    local_key=LOCAL_KEY,
    zones=json.loads(ZONES),
    debug=debug,
)


@auth.verify_password
def verify_password(username, password):
    if username in users:
        return check_password_hash(users.get(username), password)
    return False


class ResourceMixing(Resource):
    method_decorators = [auth.login_required]


# This error handler is necessary for usage with Flask-RESTful
@parser.error_handler
def handle_request_parsing_error(err, req, schema, *, error_status_code, error_headers):
    """webargs error handler that uses Flask-RESTful's abort function to return
    a JSON error response to the client.
    """
    abort(error_status_code, errors=err.messages)


class zones(ResourceMixing):
    def get(self):
        return diivoo.get()

    def post(self):
        if not request.is_json:
            return {"message": "not an application/json content type"}, 400
        content: dict = request.json
        for key in content.keys():
            diivoo.set_status(on=content[key], zone=key)


class zone(ResourceMixing):
    def get(self, zone):
        return diivoo.get()[zone]


class zone_status(ResourceMixing):
    def post(self, zone, status):
        if status in ["on", "1"]:
            diivoo.activate(zone)
        elif status in ["off", "0"]:
            diivoo.deactivate(zone)
        else:
            return {"message": "not supported"}, 501


api.add_resource(zones, "/api/zone")
api.add_resource(zone, "/api/zone/<string:zone>")
api.add_resource(zone_status, "/api/zone/<string:zone>/<string:status>")

if __name__ == "__main__":
    app.run(debug=debug)
