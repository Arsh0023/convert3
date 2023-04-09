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
    
def createJWT(username, secret, authz):
    return jwt.encode(
        {
            "username": username,
            "exp": datetime.datetime.now(tz=datetime.timezone.utc)
            + datetime.timedelta(days=1),
            "iat": datetime.datetime.utcnow(),
            "admin": authz
        },
        secret,
        algorithm="HS256"
    )

@server.route("/validate",methods=["POST"])
def validate():
    encoded_jwt = request.headers["Authorization"]

    if not encoded_jwt:
        return "Missing Credentials", 401
    
    encoded_jwt = encoded_jwt.split(" ")

    try:
        decoded = jwt.decode(
            encoded_jwt,
            os.environ.get("JWT_SECRET"),
            algorithms="HS256"
        )
    except:
        return "Not Authorized", 403
    
    return decoded, 200

if __name__ == "__main__":
    server.run(host="0.0.0.0",port=5000)
