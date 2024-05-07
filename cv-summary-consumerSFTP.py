from kafka import KafkaConsumer
from kafka import KafkaProducer
import confluent_genai
import os
import json

pdffile  = os.environ["PDFFILE"]

# Configure Kafka Consumer
consumer = KafkaConsumer(
    'loaded-cv-files',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='latest',
    group_id='cv-summarizer'
)
# Configure Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],  # List of Kafka broker addresses
    value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Serializer for the message data
)
# Define the topic name
topic = 'cv-summaries'
# AI process function

def main():
    for message in consumer:
        # Read Bytes Data from Kafka
        msg_value = message.value
        # Transform Bytes into a temp cv.pdf file
        with open(pdffile, 'wb') as file: 
            file.write(msg_value) 
        print(f"**** MESSAGE FROM SFTP Server ****")
        print(f"Received message:")
        # ai_output = load_and_process_with_ai(msg_value)
        ai_output = confluent_genai.load_and_process_with_ai(pdffile)
        if ai_output:
            print(f"**** CV-Summary ****")
            print(f"AI processed output: {ai_output}")
            # Send a message
            message = ai_output
            print(message)
            producer.send(topic, message)
            # Wait for all messages to be sent
            #producer.flush()
            print("Message sent successfully to topic cv-summaries!")
        else:
            print("Failed to process message with AI.")
    # Optionally, close the producer
    producer.close()

if __name__ == "__main__":
    print("Start Confluent CV Summarizer Consumer from loaded_cv_files topic.")
    main()
    
    