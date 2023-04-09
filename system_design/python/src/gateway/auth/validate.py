import os, requests

#we auth_svc as it was contacting to the auth microservice.
#Now we are creating this auth package to be used internally by the gateway microservice.
#Flow is first the client will be sent to auth microservice and then for all subsequent services
#there will be authorization header in the request.

def token(request):
    if not "Authorization" in request.headers:
        return None, ("Missing Credentials", 401)
    
    token = request.headers["Authorization"]

    if not token:
        return None, ("Missing Token", 401)
    
    response = requests.post(
        f"http://{os.environ.get('AUTH_SVC_ADDRESS')}/validate",
        headers = {"Authorization": token}
    )

    if response.status_code == 200:
        pass
    else:
        pass