##research, options, and issues with the push notifications 
##not shown: one signal 


#this send locally but i cant try to change implementation until hosted 
from plyer import notification
notification.notify(
    title='Here is the title',
    message='Here is the message',
    app_name='Here is the application name'
)

##possible to use https://notify.run/
## more on notify bookmarked locally 
from notify_run import Notify 
notify = Notify() 
notify.send('idk what im doing')

# desktop notifier 
#issue with dbus
import feedparser 
import notify2 
import os 
import time 
def send_stuff(): 
    ICON_PATH = os.getcwd() + "/icon.ico"
    notify2.init('test test test') 
    n = notify2.Notification('test',  
                             'tester',  
                             icon=ICON_PATH  
                             ) 
    n.set_urgency(notify2.URGENCY_NORMAL) 
    n.show() 
    n.set_timeout(15000) 
    time.sleep(1200) 

#!/usr/bin/python
import gi
gi.require_version('Gio', '2.0')
from gi.repository import Gio

Application = Gio.Application.new("hello.world", Gio.ApplicationFlags.FLAGS_NONE)
Application.register()
Notification = Gio.Notification.new("Hello world")
Notification.set_body("This is an example notification.")
Icon = Gio.ThemedIcon.new("dialog-information")
Notification.set_icon(Icon)
Application.send_notification(None, Notification)

##original code from notify run 
##wont work completely until it is hosted 
##this code works with flask 
from pywebpush import webpush

#from notify_run_server.params import VAPID_PRIVKEY, VAPID_EMAIL
from config import VAPID_PUBLIC_KEY, VAPID_PRIVATE_KEY, VAPID_ADMIN_EMAIL
from multiprocessing import Process
import json


def parallel_notify(subscriptions, message, channel_id, data, **params):
    procs = list()
    for subscription in subscriptions:
        message_json = json.dumps({
            'message': message,
            'channel': channel_id,
            'data': data,
            **params
        })
        print(message_json)

        p = Process(target=notify, args=(subscription, message_json))
        p.start()
        procs.append(p)

    for p in procs:
        p.join()


def notify(subscription, data):
    VAPID_PARAMS = {
        'vapid_private_key': VAPID_PRIVATE_KEY,
        'vapid_claims': {'sub': 'mailto:{}'.format(VAPID_ADMIN_EMAIL)}
    }

    try:
        r = webpush(
            subscription_info=subscription,
            data=data,
            timeout=10,
            **VAPID_PARAMS
        )
    except:
        pass

##model.py
from abc import ABC, abstractmethod
from datetime import datetime
from random import choice
from typing import List

import boto3
import dateutil.parser
from boto3.dynamodb.conditions import Key

from notify_run_server.params import CHANNEL_ID_CHARS, CHANNEL_ID_LENGTH, MESSAGE_TABLE, CHANNEL_TABLE, VAPID_PUBKEY


class NoSuchChannel(Exception):
    def __init__(self, channel_id):
        self.channel_id = channel_id


class NotifyModel:
    def __init__(self):
        dynamodb = boto3.resource('dynamodb')
        self._message_table = dynamodb.Table(MESSAGE_TABLE)
        self._channel_table = dynamodb.Table(CHANNEL_TABLE)

    def register_channel(self, meta: dict) -> str:
        channel_id = ''.join(choice(CHANNEL_ID_CHARS)
                             for _ in range(CHANNEL_ID_LENGTH))
        self._channel_table.put_item(Item={
            'channelId': channel_id,
            'created': str(datetime.now()),
            'meta': meta,
            'subscriptions': {},
        })
        return channel_id

    def add_subscription(self, channel_id: str, subscription: dict):
        id = subscription['id']
        self._channel_table.update_item(
            Key={'channelId': channel_id},
            UpdateExpression='SET #s.#k = :new_sub',
            ExpressionAttributeNames={
                '#s': 'subscriptions',
                '#k': id,
            },
            ExpressionAttributeValues={
                ':new_sub': subscription['subscription']
            }
        )

    def get_channel(self, channel_id: str):
        result = self._channel_table.query(
            KeyConditionExpression=Key('channelId').eq(channel_id)
        )
        if result['Count'] != 1:
            raise NoSuchChannel(channel_id)
        return result['Items'][0]

    def _check_valid_channel(self, channel_id: str) -> bool:
        result = self._channel_table.query(
            KeyConditionExpression=Key('channelId').eq(channel_id)
        )
        return result['Count'] > 0

    def _assert_valid_channel(self, channel_id: str):
        if not self._check_valid_channel(channel_id):
            raise NoSuchChannel(channel_id)

    def get_messages(self, channel_id: str) -> List[dict]:
        self._assert_valid_channel(channel_id)
        result = self._message_table.query(
            KeyConditionExpression=Key('channelId').eq(channel_id),
            ScanIndexForward=False,
            Limit=10,
        )
        items = result['Items']
        return [
            {
                'message': item['message'],
                'time': dateutil.parser.parse(item['messageTime'])
            } for item in items]

    def put_message(self, channel_id: str, message: str, data: dict):
        self._message_table.put_item(
            Item={
                'channelId': channel_id,
                'messageTime': str(datetime.now()),
                'message': message,
                'data': data,
            })