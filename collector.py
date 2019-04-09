#!/usr/bin/env python3.6

import os
import sys
from getpass import getpass
from time import sleep
from datetime import datetime

from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.errors.rpc_errors_400 import UsernameNotOccupiedError
from telethon.errors.rpc_errors_420 import FloodWaitError
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.functions.contacts import ResolveUsernameRequest
from telethon.tl.types import ChannelParticipantsSearch, InputChannel
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.functions.users import GetUsersRequest

# First you need create app on https://my.telegram.org
api_id = 12834
api_hash = 'c84d9229db1d6be95c067b02b126352c'
phone = '+77778178413'
limit = 200
with open ('chats_list.txt') as file:
    chats_list=file.readlines()

with open ('alphabet.txt') as file:
    alphabet=file.readlines()

def get_chat_info(username, client):
    try:
        chat = client(ResolveUsernameRequest(username))
    except UsernameNotOccupiedError:
        print('Chat/channel not found!')
        sys.exit()
    result = {
        'chat_id': chat.peer.channel_id,
        'access_hash': chat.chats[0].access_hash
    }
    return result

def dump_users(chat, client, chat_name, letter):
    counter = 0
    offset = 0
    chat_object = InputChannel(chat['chat_id'], chat['access_hash'])
    all_participants = []
    print(f'Process... letter: {letter}')
    while True:
        participants = client.invoke(GetParticipantsRequest(
                    chat_object, ChannelParticipantsSearch(letter), offset, limit
                ))
        if not participants.users:
            break
        all_participants.extend(['{} {}'.format(x.username, x.status)
                           for x in participants.users])
        users_count = len(participants.users)
        offset += users_count
        counter += users_count
        print('{} users collected'.format(counter))
        #sleep(0.5)
    with open(f'{chat_name}_users.txt', 'a') as file:
        file.write('\n'.join(map(str, all_participants)))

def participants_count(client, chat):
     chat_object = InputChannel(chat['chat_id'], chat['access_hash'])
     chat_full = client.invoke(GetFullChannelRequest(chat_object))
     part_count = chat_full.full_chat.participants_count
     print(f'Participants count: {part_count}')
     return (part_count)

def main():
    for chat_name in chats_list:
        chat_name = chat_name.replace('\n', '')
        client = TelegramClient('current-session', api_id, api_hash)
        print('Connecting...')
        print(f'Chat: {chat_name}')
        client.connect()
        if not client.is_user_authorized():
            try:
                client.send_code_request(phone)
                print('Sending a code...')
                client.sign_in(phone, code=input('Enter code: '))
                print('Successfully!')
            except FloodWaitError as FloodError:
                print('Flood wait: {}.'.format(FloodError))
                sys.exit()
            except SessionPasswordNeededError:
                client.sign_in(password=getpass('Enter password: '))
                print('Successfully!')
                print(participants_count)
        if participants_count(client, get_chat_info(chat_name, client)) > 11000:
            for letter in alphabet:
                letter = letter.replace('\n', '')
                dump_users(get_chat_info(chat_name, client), client, chat_name, letter)
        else:
            dump_users(get_chat_info(chat_name, client), client, chat_name, '')
        print('Done!')

if __name__ == '__main__':
    main()



