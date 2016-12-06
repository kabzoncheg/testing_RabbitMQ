import json
import uuid

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='netconf_workers',type='direct')

host = '10.0.1.2'
trans_id = uuid.uuid1().int
manual_update_flag = False

message_as_dict = {'db_update':{'host':host, 'transaction_id':trans_id, 'manual_update_flag': manual_update_flag}}
message = json.dumps(message_as_dict, sort_keys=True)
channel.basic_publish(exchange='netconf_workers', routing_key='db_update', body=message,
                      properties=pika.BasicProperties(content_type='application/json'))
print(" [x] Sent %r" % message)
connection.close()
