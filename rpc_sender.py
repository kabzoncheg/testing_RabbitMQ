import json
import uuid
from time import time

import pika

class SendRPC(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()

        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(self.on_response, no_ack=True, queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.time_smpl = time()
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key='rpc_queue',
                                   properties=pika.BasicProperties(
                                         reply_to = self.callback_queue,
                                         correlation_id = self.corr_id,
                                         ),
                                   body=str(n))
        while self.response is None:
            self.connection.process_data_events()
            if  time() - self.time_smpl < 10:
                pass
            else:
                print('timeout!')
                break
        return self.response

host = '10.0.1.231'
trans_id = uuid.uuid1().int
manual_update_flag = False

message_as_dict = {'db_update':{'host':host, 'transaction_id':trans_id, 'manual_update_flag': manual_update_flag}}
message = json.dumps(message_as_dict, sort_keys=True)

rpc_sender = SendRPC()

print('Sending request')
response = rpc_sender.call(message)
print('Response:', response)


