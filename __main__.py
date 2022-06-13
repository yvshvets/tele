import os
import sys

import requests
from telethon import TelegramClient
from telethon.errors import FloodWaitError, PeerFloodError, PhoneNumberBannedError
from telethon.tl.functions.account import UpdateProfileRequest, SetPrivacyRequest
from telethon.tl.functions.contacts import ImportContactsRequest
from telethon.tl.functions.photos import UploadProfilePhotoRequest
from telethon.tl.types import InputPhoneContact, InputPrivacyKeyPhoneNumber, \
    InputPrivacyValueDisallowAll, InputPrivacyKeyAddedByPhone, InputPrivacyValueAllowContacts

session = os.environ.get('SESSION', '/home/yvshvets/IdeaProjects/spamer/infrastructure/sessions/test/628385586504')
api_id = os.environ.get('API_ID', 10840)
hash_key = os.environ.get('HASH_KEY', '33c45224029d59cb3ad0c16134215aeb')
command = os.environ.get('COMMAND', 'init_account')
params = os.environ.get('JSON', '{}')
phone = os.environ.get('PHONE', '628385586504')
password = os.environ.get('PASSWORD', '')
# code = os.environ.get('CODE', '72861')
code = os.environ.get('CODE', None)
# session = os.environ.get('SESSION', '')
# api_id = os.environ.get('API_ID', 0)
# hash_key = os.environ.get('HASH_KEY', '')
# command = os.environ.get('COMMAND', '')
param_text = os.environ.get('PARAM_TEXT', 'ROYAL BONUS до 150 FS по ставці до 32 грн за удар, у грі "Golden Reel" Иван, насолоджуйтесь грою в казино "Dragon`s Gold"! https://bit.ly/3x4GYy4')
# param_image = os.environ.get('PARAM_IMAGE', 'https://media.user.com/uploads/pt38gj-dragon-sgold/telega-3_n2lV6ku.jpg')
param_image = os.environ.get('PARAM_IMAGE', 'https://dragongold88.com/api/media/images/banner-desktop/e24c74c245cd0857271eef20e7a9df4894e0f49522a0d8073f7aa599a14a3f68.jpg')
param_phone = os.environ.get('PARAM_PHONE', '380675323902')
param_name = os.environ.get('PARAM_NAME', 'Drag0ns')
param_last_name = os.environ.get('PARAM_LAST_NAME', 'Go1d')
# phone = os.environ.get('PHONE', '')
# password = os.environ.get('PASSWORD', '')
# code = os.environ.get('CODE', None)

client: TelegramClient
try:
    client = TelegramClient(session, api_id, hash_key)
except PhoneNumberBannedError as err:
    print(err)
    sys.exit(33)

if code:
    print("Start login")
    try:
        client.start(phone=phone, password=password, code_callback=lambda: code)
    except PhoneNumberBannedError as err:
        print(err)
        sys.exit(33)
else:
    print("Start get login code")
    try:
        client.start(phone=phone, code_callback=lambda: sys.exit(50))
    except PhoneNumberBannedError as err:
        print(err)
        sys.exit(33)


async def main():
    if command == '':
        await add_user()
        return await send_message()
    if command == 'add_user':
        return await add_user()
    if command == 'send_message':
        return await send_message()
    if command == 'init_account':
        return await init_account()
    if command == 'check_auth':
        return await check_auth()


async def check_auth():
    print(await client.get_me())
    sys.exit(0)


async def add_user():
    try:
        print("Start invite user " + param_phone)
        user = InputPhoneContact(0, param_phone, '', '')
        contact = await client(ImportContactsRequest([user]))
        print(contact)
        if len(contact.imported) == 0 and len(contact.users) == 0 and\
                len(contact.popular_invites) == 0 and len(contact.retry_contacts) == 1:
            print("Error account locked: {}".format(param_phone))
            sys.exit(33)
        if len(contact.users) == 0:
            print("Error invite contact phone: {}".format(param_phone))
            sys.exit(3)
    except PeerFloodError as err:
        print(err)
        sys.exit(13)
    except FloodWaitError as err:
        print(err)
        sys.exit(16)
    except PhoneNumberBannedError as err:
        print(err)
        sys.exit(33)


async def send_message():
    try:
        if param_image:
            b = requests.get(param_image)
            file = await client.upload_file(b.content)
            res = await client.send_file(param_phone, file, caption=param_text, parse_mode='md')
            if res.id:
                print("Sent image id: {} to {}".format(res.id, res.peer_id))
                sys.exit(0)
        else:
            res = await client.send_message(param_phone, param_text, parse_mode='md')
            if res.id:
                print("Sent message id: {} to {}".format(res.id, res.peer_id))
    except FloodWaitError as err:
        print(err)
        sys.exit(16)
    except PeerFloodError as err:
        print(err)
        sys.exit(13)
    except PhoneNumberBannedError as err:
        print(err)
        sys.exit(33)


async def init_account():
    print("init account with hide number")
    print("init account name {} and last name {} and foto".format(param_name, param_last_name, param_image))
    await client(UpdateProfileRequest(first_name=param_name, last_name=param_last_name, about='https://dragongold88.com'))
    b = requests.get(param_image)
    file = await client.upload_file(b.content)
    await client(UploadProfilePhotoRequest(await client.upload_file(file)))
    await client(SetPrivacyRequest(InputPrivacyKeyPhoneNumber(), [InputPrivacyValueDisallowAll()]))
    await client(SetPrivacyRequest(InputPrivacyKeyAddedByPhone(), [InputPrivacyValueAllowContacts()]))
    print(await client.get_me())
    sys.exit(0)


with client:
    client.loop.run_until_complete(main())
