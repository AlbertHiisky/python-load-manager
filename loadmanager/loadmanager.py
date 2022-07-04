# today many services will die

from flask import Flask, request
import requests
import yaml
from server import Server


def load_configuration(file_path):
    with open(file_path) as config_file:
        conf = yaml.load(config_file, Loader=yaml.FullLoader)
        return conf


def load_servers_from_config(conf):
    servers = []
    for i in conf["servers"]:
        servers.append(Server(i))
    return servers


def get_least_loaded_server(servers):
    if not servers:
        return None
    else:
        return min(servers, key=lambda x: x.open_connections)


def get_living_servers(servers):
    alive_servers = []
    for server in servers:
        server.healthcheck()
        if server.healthy:
            alive_servers.append(server)
    return alive_servers


loadbalancer = Flask(__name__)
config = load_configuration('config.yaml')
servers = load_servers_from_config(config)


@loadbalancer.route("/")
def router():
    alive_servers = get_living_servers(servers)
    if not alive_servers:
        return "No Backends servers available", 503
    server_to_forward = get_least_loaded_server(alive_servers)
    server_to_forward.open_connections += 1
    response = requests.get("http://{}{}".format(server_to_forward.endpoint, "/"))
    server_to_forward.open_connections -= 1
    return response.content, response.status_code


if __name__ == '__main__':
    loadbalancer.run(host="0.0.0.0", debug=True, port=5000)
