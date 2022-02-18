#!/usr/bin/env python3.8

from telethon.sync import TelegramClient
from telethon import functions, types
from telethon import types
from datetime import datetime
from datetime import timedelta
import os

client = TelegramClient('my_connect', 12834, 'c84d9229db1d6be95c067b02b126352c')
limit = 100
days_of_activity = 7
alphabet = ('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z')
with open ('chats_list.txt') as file:
    chats_list=file.readlines()

async def parser(chat, letter):
    counter = 0
    offset = 0
    all_participants = []
    while True:
        participants = await client(functions.channels.GetParticipantsRequest(channel = chat, filter = types.ChannelParticipantsSearch(letter), offset = offset, limit = limit, hash = 0))
        if not participants.users:
            break
        for x in participants.users:
            if x.username != None:
                all_participants.append([x.username, x.status])
        users_count = len(participants.users)
        counter += users_count
        offset += users_count
        print(f'users collected {counter}')
    return all_participants

def save_result(participants, days, chatname):
    time_limit = (datetime.utcnow() - timedelta(days=days)).strftime('%Y-%m-%d %H:%M:%S')
    users_recently = []
    users_actual = []
    users_other = []
    for participant in participants:
        try:
            if str(participant[1]).startswith('UserStatusRecen'):
                users_recently.append(participant[0])
            elif str(participant[1]).startswith('UserStatusOnline'):
                users_actual.append(participant[0])
            elif participant[1].was_online.strftime('%Y-%m-%d %H:%M:%S') >= time_limit:
                users_actual.append(participant[0])
            else:
                users_other.append(participant[0])
                pass
        except: 
            pass
    try:
        os.makedirs(f'./{chatname}')
    except FileExistsError:
        pass
    del_double_recently = list(set(users_recently))
    del_double_actual = list(set(users_actual))
    del_double_other = list(set(users_other))
    print(f'Users_recently: {len(del_double_recently)}')
    with open(f'{chatname}/users_recently.txt', 'a') as file:
        file.write('\n'.join(map(str, users_recently)))
    print(f'Users_actual: {len(del_double_actual)}')
    with open(f'{chatname}/users_actual.txt', 'a') as file:
        file.write('\n'.join(map(str, del_double_actual)))
    print(f'Users_other: {len(del_double_other)}')
    with open(f'{chatname}/users_other.txt', 'a') as file:
        file.write('\n'.join(map(str, del_double_other)))

async def main():
    for chat_name in chats_list:
        chat_name = chat_name.replace('\n', '')
        chat_info = await client(functions.channels.GetFullChannelRequest(chat_name))
        number_participants = chat_info.full_chat.participants_count
        print(f'Chat name: {chat_name}. Number of users: {number_participants}')
        if number_participants > 11000:
            print('Alphabetical work')
            joinusers = []
            for letter in alphabet:
                print(f'Letter: {letter}')
                users = await parser(chat_name, letter)
                joinusers += users
            save_result(joinusers, days_of_activity, chat_name)
        else:
            print('Ordinary work')
            users = await parser(chat_name, '')
            save_result(users, days_of_activity, chat_name)

with client:
    client.loop.run_until_complete(main())


