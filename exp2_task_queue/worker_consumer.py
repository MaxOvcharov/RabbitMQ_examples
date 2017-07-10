# -*- coding: utf-8 -*-
import json
import pika
import time

from optparse import OptionParser


def parse_args_for_init_worker():
    """
    Configurations of arg-parser for init worker
    :return: options - a dict with input args
    """
    parser = OptionParser()
    parser.add_option('-d', '--delay', dest='callback_delay',
                      help='ADDING DELAY INTO CALLBACK FUNCTION',
                      type='int', default=None)
    parser.add_option('-w', '--worker', dest='worker_number',
                      help='CREATE NUMBER OF WORKERS',
                      type='int', default=1)
    options, args = parser.parse_args()

    return options

opt = parse_args_for_init_worker()
callback_delay = opt.callback_delay
worker_number = opt.worker_number
task_counter = 1

conn = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = conn.channel()
channel.queue_declare(queue='task_queue', durable=True)
print(' [*] Waiting for messages. Delay:{0}, Number of workers: {1}.\n'
      ' To exit press CTRL+C'.format(callback_delay, worker_number))


def callback(ch, method, properties, body):
    global task_counter
    client_message = json.loads(body)
    print(' [x] Received: %s, message_type: %s' % (client_message,
                                                   type(client_message)))
    if callback_delay:
        time.sleep(callback_delay)
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print('DONE TASK: {}'.format(task_counter))
    task_counter += 1


channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback, queue='task_queue')
channel.start_consuming()
