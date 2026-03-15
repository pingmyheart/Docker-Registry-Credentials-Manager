import signal
import sys

from flask import Flask
from flask_cors import CORS

from configuration.logging_configuration import logger as log
from controller import blueprints

app = Flask(__name__)
CORS(app)

for blueprint in blueprints:
    app.register_blueprint(blueprint)


def handle_signal(signum, frame):
    log.info(f"Received signal {signum}, shutting down...")
    # Perform cleanup here
    sys.exit(0)


signal.signal(signal.SIGINT, handle_signal)  # CTRL+C
signal.signal(signal.SIGTERM, handle_signal)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True, use_reloader=False)
