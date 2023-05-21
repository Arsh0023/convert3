import os, gridfs, pika, json
from flask import Flask, request, send_file
from flask_pymongo import PyMongo
from auth import validate
from auth_svc import access
from storage import util
from bson.objectid import ObjectId

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
    
@server.route("/upload", methods=["POST"])
def upload():
    access, err = validate.token(request)

    access = json.loads(access)

    if access["admin"]:
        if len(request.files) != 1:
            return "Exactly One File required", 400
        
        for _, f in request.files.items():
            err = util.upload(f, fs, channel, access) #channel here is for rabbitMQ

            if err:
                return err
        return "success!", 200
    else:
        return "Not authorized", 401
    
@server.route('/download', methods=["POST"])
def download():
    access, err = validate.token(request)

    access = json.loads(access)

    if access["admin"]:
        fid_string = request.args.get("fid")

        if not fid_string:
            return "fid is required", 400
        
        try:
            out = fs_mp3s.get(ObjectId(fid_string))
            return send_file(out, download_name=f'{fid_string}.mp3')
        except Exception as err:
            print(err)
            return "Internal Server Error", 500

    return "Not Authorized", 401

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=8080)