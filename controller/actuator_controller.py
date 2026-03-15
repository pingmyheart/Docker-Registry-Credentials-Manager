from flask import Blueprint, jsonify

from configuration.logging_configuration import logger as log

actuator_bp = Blueprint('actuator', __name__, url_prefix='/actuator')


@actuator_bp.route('/health', methods=['GET'])
def health():
    log.info("[INCOMING REQUEST] - Health actuator")
    response = __response()
    return jsonify(response), 200 if response["status"] == "UP" else 503


@actuator_bp.route('/readiness', methods=['GET'])
def readiness():
    log.info("[INCOMING REQUEST] - Ready actuator")
    response = __response()
    return jsonify(response), 200 if response["status"] == "UP" else 503


def __response():
    return {
        "status": "UP"
    }
