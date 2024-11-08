#!/usr/bin/env python
import pika, sys, os

rabbitmq_host = 'dev-azimuth-rabbitmq-cluster-nonlive-0.dev-azimuth-rabbitmq-cluster-nonlive-headless.rabbitmq-system.svc.cluster.local'
rabbitmq_port = 5672 
rabbitmq_user = 'user'
rabbitmq_password = 'AmYoFHCzMF1V2C8x'

def main():
    # Create a credentials object
    credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)

    # Define connection parameters
    connection_params = pika.ConnectionParameters(
        host=rabbitmq_host,
        port=rabbitmq_port,
        credentials=credentials
    )
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()

    channel.queue_declare(queue='hello')

    def callback(ch, method, properties, body):
        print(f" [x] Received {body}")

    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)