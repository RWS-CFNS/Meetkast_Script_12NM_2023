#!/usr/bin/env python
import csv 
import pika  


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost')) 

channel = connection.channel() 
  

channel.queue_declare(queue='hello') 


channel.basic_publish(exchange='', 

                      routing_key='hello', 

                      body='Hello World!') 

print(" [x] Sent 'Hello World!'") 

  

# Stel de RabbitMQ-server in 

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost')) 

channel = connection.channel() 

  
# Maak een uitwisseling (exchange) genaamd 'csv_exchange' (kies het juiste type, bijv. 'direct', 'fanout', 'topic', etc.) 

channel.exchange_declare(exchange='csv_exchange', exchange_type='direct') 


# Lees het invoer-CSV-bestand 

input_file = 'input.csv' 

output_file = 'output.csv' 


with open(input_file, 'r') as csv_in: 

    csv_reader = csv.reader(csv_in) 

    for row in csv_reader: 

        # Verstuur elk rijtje naar RabbitMQ 

        message = ','.join(row) 

        channel.basic_publish(exchange='csv_exchange', routing_key='', body=message) 


# Sluit de verbinding met RabbitMQ 

connection.close() 

# Schrijf de gegevens naar het uitvoer-CSV-bestand 

with open(output_file, 'w', newline='') as csv_out: 

    csv_writer = csv.writer(csv_out) 

    # Hier kun je de gegevens ontvangen van RabbitMQ en schrijven naar het uitvoer-CSV-bestand, indien nodig. 
