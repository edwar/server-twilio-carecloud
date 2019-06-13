from flask import Flask
from flask import jsonify
from flask import request

import ujson

application = Flask(__name__)

@application.route('/')
def hello_world():
    return 'Hello, World!'
    


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

    ACCOUNT_SID = account_sid
    API_KEY_SID = 'SK08e688a95ac12a599a36deb2aec64a68'
    API_KEY_SECRET = 'akrwxUmAompQjVNnpExLgOkMAf2m45iC'

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

    ACCOUNT_SID = 'AC0899dfbac4d4374a162ad3f494a29cb9'
    API_KEY_SID = 'SK0d73ceea012fd7a740cfea97b091b11f'
    API_KEY_SECRET = '9c2gxH04Fd2RNV9EePMYW1XmeNP1ehOm'

    # Create an Access Token
    token = AccessToken(ACCOUNT_SID, API_KEY_SID, API_KEY_SECRET, identity=name)


    # Grant access to Video
    grant = VideoGrant(room=room)
    token.add_grant(grant)


    print(token.to_jwt())

    return ujson.dumps({
        'token': token.to_jwt(), 
        'name': name, 
        'room': room
        })

if __name__ == '__main__':
    application.run(host='0.0.0.0')