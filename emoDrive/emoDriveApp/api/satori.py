#!/usr/bin/env python

from __future__ import print_function
import sys
import threading

import sys
sys.path.insert(0, '../');
from app_settings import *

from satori.rtm.client import make_client, SubscriptionMode

channel = SATORI_CHANNEL
endpoint = SATORI_CHANNEL_API_ENDPOINT
appkey = SATORI_API_KEY


class Message():

    def __init__(self):
        self.messages = []
        self.got_message_event = threading.Event()


    def poll(self, mailbox):
        while(True):
            if not self.got_message_event.wait(30):
                print("Timeout while waiting for a message")

            self.messages.extend(mailbox)
            self.got_message_event.clear()



    def start_weather_alerts(self):
        with make_client(
                endpoint=endpoint, appkey=appkey) as client:
            print('Connected!')

            mailbox = []


    class SubscriptionObserver(object):
        def on_subscription_data(self, data):
            mailbox = []
            for message in data['messages']:
                mailbox.append(message)
            self.got_message_event.set()

            subscription_observer = SubscriptionObserver()
            client.subscribe(
                channel,
                SubscriptionMode.SIMPLE,
                subscription_observer)
            t = threading.Thread(target=self.poll, args=(mailbox,))
            t.start()
