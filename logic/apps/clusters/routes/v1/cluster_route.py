from flask import Blueprint, jsonify, request
from logic.apps.clusters.models.cluster_model import Cluster
from logic.apps.clusters.services import cluster_service

blue_print = Blueprint('clusters', __name__, url_prefix='/api/v1/clusters')


@blue_print.route('/', methods=['POST'])
def post():
    s = request.json
    cluster_service.add(Cluster(
        name=s['name'],
        url=s['url'],
        token=s['token'],
        version=s['version'],
        type=s['type']
    ))
    return '', 201


@blue_print.route('/<name>', methods=['GET'])
def get(name: str):
    s = cluster_service.get(name)
    if not s:
        return '', 204

    return jsonify(s.__dict__()), 200


@blue_print.route('/', methods=['GET'])
def list_all():

    return jsonify(cluster_service.list_all()), 200


@blue_print.route('/<name>', methods=['DELETE'])
def delete(name: str):
    cluster_service.delete(name)
    return '', 200


@blue_print.route('/all/short', methods=['GET'])
def get_all_short():
    return jsonify(cluster_service.get_all_short()), 200


@blue_print.route('/<name>/test', methods=['GET'])
def test_cluster(name):
    return jsonify(cluster_service.test_cluster(name)), 200


@blue_print.route('/<name>', methods=['PUT'])
def modify_server(name):

    s = request.json
    server = Cluster(
        name=s['name'],
        url=s['url'],
        token=s['token'],
        version=s['version'],
        type=s['type']
    )
    cluster_service.modify(name, server)

    return '', 200
