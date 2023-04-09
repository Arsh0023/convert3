import os, requests
#Keep in mind that we made a small package called auth_svc to actually interact with our auth service and get responses in our own tailor made forms.
def login(request):
    auth = request.authorization
    if not auth:
        return None,("Missing Credentials",401)
    
    basicAuth = (auth.username, auth.password)

    response = requests.post(
        url=f"http://{os.environ.get('AUTH_SVC_ADDRESS')}/login",
        auth=basicAuth
    )

    if response.status_code == 200:
        return response.txt, None
    else:
        return None, (response.txt, response.status_code)
