import os, gridfs, pika, json
from flask import Flask, request
from flask_pymongo import PyMongo
from auth import validate
from auth_svc import access
from storage import util

server = Flask(__name__)
server.config["MONGO_URI"] = "mongodb://host.minikube.internal:27017/videos"

mongo = PyMongo(server)

fs = gridfs.GridFS(mongo.db)

connections = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq")) #refrencing out rabbitmq host

@server.route("/login", methods=["POST"])
def login():
    token,err = access.login(request)

    if not err:
        return token
    else:
        return err
    
@server.route("/upload",methods=["POST"])
def upload():
    access, err = validate.token(request)

    if not err:
        pass
    else:
        return err