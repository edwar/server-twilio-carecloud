from flask import Flask
from flask import jsonify
from flask import request

import ujson

application = Flask(__name__)

@application.route('/')
def hello_world():
    return 'Hello, World!'
    
@application.route('/api/twilio/auth/video')
def twilio_api_auth_video():
     from twilio.rest import Client

     # Your Account Sid and Auth Token from twilio.com/console for video
     account_sid = 'AC0899dfbac4d4374a162ad3f494a29cb9'
     auth_token = 'dcc16a90db9419c40e3a4752a8b59d31'
     client = Client(account_sid, auth_token)

     new_key = client.new_keys.create()
     auth = {
         'key': new_key.sid,
         'secret': new_key.secret
     }
     print(new_key.secret)

     return jsonify(auth)

@application.route('/api/twilio/auth/chat')
def twilio_api_auth_chat():
     from twilio.rest import Client

     # Your Account Sid and Auth Token from twilio.com/console fron chat
     account_sid = 'AC1ab30057b0be6eaaa144ff94b773c882'
     auth_token = '6ec8894a7733967f155c26d39feadf3a'
     client = Client(account_sid, auth_token)

     new_key = client.new_keys.create()
     auth = {
         'key': new_key.sid,
         'secret': new_key.secret
     }
     print(new_key.secret)

     return jsonify(auth)

@application.route('/api/twilio/chat', methods=['GET'])
def twilio_api_chat():
    from twilio.jwt.access_token import AccessToken
    from twilio.jwt.access_token.grants import ChatGrant
    from twilio.rest import Client

    service_sid = 'IScb01dd8aeded43f1961957e46cfcf717'
    identity = request.args.get('identity')

    # required for all twilio access tokens
    account_sid = 'AC1ab30057b0be6eaaa144ff94b773c882'
    auth_token = '6ec8894a7733967f155c26d39feadf3a'
    client = Client(account_sid, auth_token)

    new_key = client.new_keys.create()

    ACCOUNT_SID = account_sid
    API_KEY_SID = new_key.sid
    API_KEY_SECRET = new_key.secret

    token = AccessToken(ACCOUNT_SID, API_KEY_SID, API_KEY_SECRET, identity=identity)

    # Create an Chat grant and add to token
    chat_grant = ChatGrant(service_sid=service_sid)
    token.add_grant(chat_grant)

    print(token.to_jwt().decode('utf-8'))

    return ujson.dumps({
        'token': token.to_jwt(), 
        'identity': identity
        })

@application.route('/api/twilio/video', methods=['GET'])
def twilio_api_video():
    from twilio.jwt.access_token import AccessToken
    from twilio.jwt.access_token.grants import VideoGrant
    from twilio.rest import Client

    name = request.args.get('name')
    room = request.args.get('room')

    print(name)
    print(room)

    # Substitute your Twilio AccountSid and ApiKey details
    account_sid = 'AC0899dfbac4d4374a162ad3f494a29cb9'
    auth_token = 'dcc16a90db9419c40e3a4752a8b59d31'
    client = Client(account_sid, auth_token)

    new_key = client.new_keys.create()

    ACCOUNT_SID = account_sid
    API_KEY_SID = new_key.sid
    API_KEY_SECRET = new_key.secret

    # Create an Access Token
    token = AccessToken(ACCOUNT_SID, API_KEY_SID, API_KEY_SECRET)

    # Set the Identity of this token
    token.identity = name

    # Grant access to Video
    grant = VideoGrant(room=room)
    token.add_grant(grant)

    # Serialize the token as a JWT
    jwt = token.to_jwt()

    print(jwt)

    return ujson.dumps({
        'token': jwt, 
        'name': name, 
        'room': room
        })

if __name__ == '__main__':
    application.run(host='0.0.0.0')