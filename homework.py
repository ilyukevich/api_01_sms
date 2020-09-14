import requests, os, time, logging
from twilio.rest import Client
from dotenv import load_dotenv


logging.basicConfig(filename="sample.log", level=logging.INFO)
log = logging.getLogger("ex")
#logging.debug("This is a debug message")
#logging.info("Informational message")
#logging.error("An error has happened!")

load_dotenv()

VERSION_APP = os.getenv('version_app')
TOKEN_VK = os.getenv('token_vk')
URL_VK = 'https://api.vk.com/method'
URL_METHOD = 'users.get'

NUMBER_FROM = os.getenv('NUMBER_FROM')
NUMBER_TO = os.getenv('NUMBER_TO')

ACCOUNT_SID = os.getenv('sid_twilio')
AUTH_TOKEN = os.getenv('token_twilio')

client = Client(ACCOUNT_SID, AUTH_TOKEN)

def get_status(user_id):
    """getting user status"""
    params = {
        'user_ids': user_id,
        'v': VERSION_APP,
        'access_token': TOKEN_VK,
        'fields': 'online'
    }
    try:
        status = requests.post(f'{URL_VK}/{URL_METHOD}', params=params)
    except (requests.exceptions.RequestException,
            requests.exceptions.HTTPError,
            requests.exceptions.ConnectionError,
            requests.exceptions.Timeout) as e:
        log.error(f'{e}')
        print(f'{e}')

        # returning the user's status to VK
    return status.json()['response'][0]['online']


def sms_sender(sms_text):
    """sending a message"""
    message = client.messages.create(
        body=sms_text,
        from_=NUMBER_FROM,
        to=NUMBER_TO
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
