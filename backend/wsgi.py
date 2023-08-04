#!/usr/bin/env python3

import connexion
from flask import Flask
from flask_cors import CORS
import swagger_server.encoder as encoder
from flask_cors import CORS


app = Flask("Demo ZHAW")
app = connexion.App("Demo ZHAW", specification_dir='swagger_server/swagger/')
app.app.json_encoder = encoder.JSONEncoder
app.add_api('swagger.yaml', arguments={'title': 'Stability demo'}, pythonic_params=True)
CORS(app.app)

if __name__ == '__main__':
    app.run(port=8080, ssl_context=('swagger_server/cert.pem', 'swagger_server/key.pem'))
