#!/usr/bin/env python3

import connexion
from flask import Flask
from flask_cors import CORS
from swagger_server import encoder
from flask_cors import CORS


app = Flask(__name__)

def main():
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'Stability demo'}, pythonic_params=True)
    CORS(app.app)
    app.run(port=8080)


if __name__ == '__main__':
    main()
