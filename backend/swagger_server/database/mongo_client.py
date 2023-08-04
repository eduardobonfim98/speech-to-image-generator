from pymongo import MongoClient
from swagger_server.services.config import CONFIG
import datetime
from flask import jsonify
import os
from dotenv import load_dotenv
load_dotenv()

DATABASE_NAME = CONFIG['db']['database_name']

AUTHDB_NAME = os.getenv('DB_AUTH_DB')
SESSION_COLLECTION_NAME = CONFIG['db']['session_collection_name']

GPT3_COLLECTION = CONFIG['db']['action_collection_gpt3']
AUDIO_COLLECTION = CONFIG['db']['action_collection_audio']
STABLE_DIFFUSION_COLLECTION = CONFIG['db']['action_collection_stable_diffusion']
username = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')

client = MongoClient(
    CONFIG['db']['host'],
    CONFIG['db']['port'],
    username=username,
    password=password,
    authSource=AUTHDB_NAME
)

db = client[DATABASE_NAME]
session_collection = db[SESSION_COLLECTION_NAME]
gpt3_collection = db[GPT3_COLLECTION]
audio_collection = db[AUDIO_COLLECTION]
stable_diffusion_collection = db[STABLE_DIFFUSION_COLLECTION]

print('Mongo Ready')


def new_session():
    creation_time = datetime.datetime.utcnow()
    result = session_collection.insert_one({'creation_time': creation_time})
    inserted_id = result.inserted_id
    return jsonify({'session_id': str(inserted_id)})


routes = [{'url': '/api/new_session',
           'name': 'new_session',
           'fn': new_session,
           'methods': ['GET']}
          ]
