with make_client(endpoint=endpoint, appkey=appkey) as client:

  print('Connected!')

mailbox = []
got_message_event = threading.Event()

class SubscriptionObserver(object):
    def on_subscription_data(self, data):
        for message in data['messages']:
            mailbox.append(message)
        got_message_event.set()

subscription_observer = SubscriptionObserver()
client.subscribe(channel, SubscriptionMode.SIMPLE, subscription_observer)


if not got_message_event.wait(10):
    print("Timeout while waiting for a message")
    sys.exit(1)

for message in mailbox:
    print('Got message "{0}"'.format(message))
