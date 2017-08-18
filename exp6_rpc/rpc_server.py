# -*- coding: utf-8 -*-
"""
    Simple RPC client example implementation using pika
"""
import pika
import sys

conn = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = conn.channel()
channel.queue_declare(queue='rpc_queue')


def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)


def on_request(ch, method, props, body):
    n = int(body.decode('utf-8'))

    print(" [.] fib(%s)" % (n,))
    response = fib(n)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(
                         correlation_id=props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    try:
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(on_request, queue='rpc_queue')
        print(" [x] Awaiting RPC requests")
        channel.start_consuming()
    except KeyboardInterrupt:
        conn.close()
        sys.exit()

if __name__ == '__main__':
    main()
