# Para subir o Rabbitmq server (com o gerenciador das filas), basta executar o comando
# sbin/rabbitmq-server no terminal, dentro da pasta /usr/local.
# lista filas: sbin/rabbitmqctl list_queues

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)


channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()