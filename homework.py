import requests, os, time
from twilio.rest import Client
from dotenv import load_dotenv


load_dotenv()

def get_status(user_id):
    """getting user status"""
    token_vk = os.getenv('token_vk')
    version_app = os.getenv('version_app')
    params = {
        'user_ids': user_id,
        'v': version_app,
        'access_token': token_vk,
        'fields': 'online'
    }
    status = requests.post('https://api.vk.com/method/users.get', params=params)
    # returning the user's status to VK
    return status.json()['response'][0]['online']


def sms_sender(sms_text):
    """sending a message"""
    account_sid = os.getenv('sid_twilio')
    auth_token = os.getenv('token_twilio')
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=sms_text,
        from_=os.getenv('NUMBER_FROM'),
        to=os.getenv('NUMBER_TO')
    )
    # returning the sid of the sent message from Twilio
    return message.sid


if __name__ == "__main__":
    vk_id = input("Enter VK user id: ")
    while True:
        if get_status(vk_id) == 1:
            sms_sender(f'User {vk_id} online now!')
            break
        time.sleep(5)
