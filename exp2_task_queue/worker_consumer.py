# -*- coding: utf-8 -*-
"""
    Simple task consumer(worker) example implementation using pika.
"""
import json
import pika
import time
import sys

from optparse import OptionParser


def parse_args_for_init_worker():
    """
    Configurations of arg-parser for init worker
    :return: options - a dict with input args
    """
    parser = OptionParser()
    parser.add_option('-d', '--delay', dest='callback_delay',
                      help='ADDING DELAY INTO CALLBACK FUNCTION',
                      type='int', default=0)
    options, args = parser.parse_args()

    return options

opt = parse_args_for_init_worker()
callback_delay = opt.callback_delay
task_counter = 1

conn = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = conn.channel()
channel.queue_declare(queue='task_queue', durable=True)
print(' [*] Waiting for messages. Delay:{0}.\n To exit press CTRL+C'.
      format(callback_delay))


def callback(ch, method, properties, body):
    global task_counter
    client_message = json.loads(body)
    print(' [x] Received: {0}, message_type: {1}'.format(client_message,
                                                         type(client_message)))
    if callback_delay:
        time.sleep(callback_delay)
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print('DONE TASK: {}'.format(task_counter))
    task_counter += 1


def main():
    try:
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(callback, queue='task_queue')
        channel.start_consuming()
    except KeyboardInterrupt:
        conn.close()
        sys.exit()

if __name__ == '__main__':
    main()
