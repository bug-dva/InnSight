"""
This kafka producer job will generate streaming data showing real time booking record.
"""
from kafka import KafkaProducer, KafkaConsumer
import time, sys
from time import gmtime, strftime
import json

topic = 'booking'

def main():
    # set up the producer
    producer = KafkaProducer(bootstrap_servers='localhost:9092')
    # Open booking data file
    file_address = "booking.txt"
    print('Start importing booking event data...')

    with open(file_address) as f:
        for line in f:
            curtime = strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
            booking_info = line.replace('\n','').split(',')
            timestamp = booking_info[0]
            zipcode = booking_info[1]
            listing_id = booking_info[2]
            price = booking_info[3]
            msg = zipcode + ',' + price + ',' + curtime
            producer.send(topic, msg.encode('utf-8'))
            print("now it is sending... ")
    producer.flush()
    f.close()

if __name__ == '__main__':
    main()
