# -*- coding: utf-8 -*-
"""
    Simple producer example with 'topic' routing implementation using pika
"""
import pika
import json
import time
import sys


from elizabeth import Text
from random import choice

SERVER_LIST = ['s1', 's2', 's3']
MSG_TYPE = ['sendMessage', 'sendHistory', 'sendCallback']

conn = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = conn.channel()
channel.exchange_declare(exchange='topic_message', exchange_type='topic')


def send_msg(payload, routing_key):
    channel.basic_publish(exchange='topic_message', routing_key=routing_key, body=payload)
    print(' [x] Send: {0}, message_type: {1}, routing_key: {2}'.format(payload, type(payload),
                                                                       routing_key))


def main():
    try:
        client_msg = Text()
        payload = dict(message=None, msg_id=0)
        msg_count = 1
        while True:
            payload['message'] = client_msg.sentence()
            payload['msg_id'] = msg_count
            routing_key = choice(SERVER_LIST) + '.' + choice(MSG_TYPE)
            send_msg(json.dumps(payload), routing_key)
            msg_count += 1
            time.sleep(1)
    except KeyboardInterrupt:
        conn.close()
        sys.exit()

if __name__ == '__main__':
    main()
