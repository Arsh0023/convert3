import jwt,datetime,os
from flask import Flask, request
from flask_mysqldb import MySQL


server = Flask(__name__)
mysql = MySQL(server)

#Config
server.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
server.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
server.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
server.config["MYSQL_PORT"] = os.environ.get("MYSQL_PORT")


@server.route("/login", methods=["POST"])
def login():
    auth = request.authorization
    if not auth:
        return "Missing Credentials", 401
    
    cur = mysql.connection.cursor()
    res = cur.execute (
        f'SELECT email,password FROM user WHERE email={auth.username}'
    )

    if res > 0: #this means the user exist within out databse every important to write such checks
        user_row = res.fetchone() #will fetch us the result row
        user = user_row[0]
        password = user_row[1]

        if user != auth.username or password != auth.password:
            return "Invalid credentials", 401
        else:
            return createJWT(auth.username, os.environ.get('JWT_SECRET'), True)
    else:
        return "Invalid Credentials", 401
