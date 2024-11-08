#!/usr/bin/env python
import pika


rabbitmq_host = 'dev-azimuth-rabbitmq-cluster-nonlive-0.dev-azimuth-rabbitmq-cluster-nonlive-headless.rabbitmq-system.svc.cluster.local'
rabbitmq_port = 5672 
rabbitmq_user = 'user'
rabbitmq_password = 'AmYoFHCzMF1V2C8x'

# Create a credentials object
credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)

# Define connection parameters
connection_params = pika.ConnectionParameters(
    host=rabbitmq_host,
    port=rabbitmq_port,
    credentials=credentials
)

# Establish connection to RabbitMQ
try:
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()
    
    print("Connected to RabbitMQ successfully!")
    
    # Example of creating a queue
    channel.queue_declare(queue='hello')

    countries_and_code = {
        'CANADA': 'CA',
        'FRANCE': 'FR',
        'GERMANY': 'DE',
        'GREECE': 'GR',
        'HONG KONG': 'HK',
        'ICELAND': 'IS',
        'INDIA': 'IN',
        'INDONESIA': 'ID',
        'IRAN, ISLAMIC REPUBLIC OF': 'IR',
        'JAPAN': 'JP',
        'KUWAIT': 'KW',
        'LUXEMBOURG': 'LU',
        'MADAGASCAR': 'MG',
        'MALDIVES': 'MV',
        'MAURITIUS': 'MU',
        'NEPAL': 'NP',
        'NEW ZEALAND': 'NZ',
        'QATAR': 'QA',
        'SAUDI ARABIA': 'SA',
        'SWITZERLAND': 'CH',
        'TURKEY': 'TR',
        'UNITED ARAB EMIRATES': 'AE',
        'UNITED KINGDOM': 'GB',
        'UNITED STATES': 'US'
    }

    for country in countries_and_code:
        channel.basic_publish(exchange='', routing_key='hello', body=f"Hello ${country}",properties=pika.BasicProperties(delivery_mode=2,))
        print(" [x] Sent 'Hello World!'")
    
    # Close the connection
    connection.close()
    print("Connection closed.")
    
except Exception as e:
    print(f"Failed to connect to RabbitMQ: {e}")