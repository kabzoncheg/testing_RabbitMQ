import json
import uuid

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.exchange_declare(exchange='netconf_workers',type='direct')

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='netconf_workers', queue=queue_name, routing_key='db_update')
print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    if isinstance(body,bytes):
        data = body.decode('utf-8')
    else:
        data = body
    result = json.loads(data)
    print(result['db_update'])

channel.basic_consume(callback, queue=queue_name, no_ack=True)

channel.start_consuming()