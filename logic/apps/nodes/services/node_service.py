import urllib.request
from typing import Dict, List

from logic.apps.nodes.errors.node_error import NodeError
from logic.apps.nodes.models.node_model import Node
from logic.libs.exception.exception import AppException
from logic.libs.logger.logger import logger

_NODES_ONLINE: Dict[str, Node] = {}


def add(node: Node):

    global _NODES_ONLINE

    if node in _NODES_ONLINE.values():
        msj = f'Ya existe un nodo con el id {node.id}'
        raise AppException(NodeError.NODE_ALREADY_EXIST_ERROR, msj)

    id = node.id
    _NODES_ONLINE[id] = node


def delete(id: str):
    global _NODES_ONLINE

    _NODES_ONLINE = {
        (k, v)
        for k, v in _NODES_ONLINE.items()
        if k != id
    }


def get(id: str) -> Node:
    global _NODES_ONLINE

    if id not in _NODES_ONLINE.keys():
        msj = f'No existe nodo con el id {id}'
        raise AppException(NodeError.NODE_NOT_EXIST_ERROR)

    return _NODES_ONLINE[id]


def is_alive(id: str) -> bool:

    node = get(id)

    try:
        url_alive = node.get_url()
        return urllib.request.urlopen(url_alive).getcode() == 200

    except Exception as e:
        logger().exception(e)
        return False


def get_by_type(type: str) -> List[Node]:
    global _NODES_ONLINE

    return [
        n
        for n in _NODES_ONLINE.values()
        if n.type == type
    ]


def list_all() -> Dict[str, Node]:
    return _NODES_ONLINE
