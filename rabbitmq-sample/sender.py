# Para subir o Rabbitmq server (com o gerenciador das filas), basta executar o comando
#  sbin/rabbitmq-server no terminal, dentro da pasta /usr/local.
# lista filas: sbin/rabbitmqctl list_queues

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
channel = connection.channel()

channel.queue_declare(queue='hello')


for x in range(10000):
    channel.basic_publish(exchange='', routing_key='hello', body=str(x) + ' Hello World!')
    print(str(x) + " [x] Sent 'Hello World!'")

connection.close()