from kafka import KafkaProducer
import json

producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda m: json.dumps(m).encode('ascii'))

def send_website_data(website_list):
    for website in website_list:
        producer.send('website_data', {'website_url': website, 'data': 'some data'})

