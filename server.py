from bottle import route, run, template, get, static_file, response, request
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import ChatGrant

# required for all twilio access tokens
account_sid = 'ACxxxxxxxxxxxx'
api_key = 'SKxxxxxxxxxxxx'
api_secret = 'xxxxxxxxxxxxxx'

# required for Chat grants
service_sid = 'ISxxxxxxxxxxxx'

@route('/hello')
def hello():
    return "Hello World!"

@route('/')
def top():
    return template('./index')

@get('/getToken')
def getToken():
    identity = request.query.get('identity')

    if identity == '':
        response.status = 400
        return 'getToken requires an Identity to be provided'

    # Create access token with credentials
    token = AccessToken(account_sid, api_key, api_secret, identity=identity)

    # Create an Chat grant and add to token
    chat_grant = ChatGrant(service_sid=service_sid)
    token.add_grant(chat_grant)
    return (token.to_jwt())

# Static file
@get("/css/<filepath:re:.*\.css>")
def css(filepath):
    return static_file(filepath, root="views/css")

@get("/js/<filepath:re:.*\.js>")
def js(filepath):
    return static_file(filepath, root="views/js")

run(host='localhost', port=8080, debug=True)