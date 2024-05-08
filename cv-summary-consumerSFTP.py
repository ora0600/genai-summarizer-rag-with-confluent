from kafka import KafkaConsumer, KafkaProducer
import confluent_genai
import os
import json

pdffile = os.getenv("PDFFILE", "default_cv.pdf")
if not pdffile:
    raise ValueError("PDFFILE environment variable is not set")

# Configure Kafka Consumer
consumer = KafkaConsumer(
    'loaded-cv-files',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='latest',
    group_id='cv-summarizer-sftp'
)

# Configure Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Define the topic name
topic = 'cv-summaries'

def main():
    try:
        # consumer from topic loaded-cv-files
        for message in consumer:
            msg_value = message.value

            # Save byted formated message value to the PDF file temp file
            with open(pdffile, 'wb') as file:
                file.write(msg_value)

            print(f"**** MESSAGE FROM SFTP Server ****")
            print(f"Received message:")

            # Process PDF with AI function
            ai_output = confluent_genai.load_and_process_with_ai(pdffile)

            if ai_output:
                print(f"**** CV-Summary ****")
                print(f"AI processed output: {ai_output}")

                # Send processed data to the new Kafka topic
                producer.send(topic, ai_output)
                producer.flush()  # Ensure all messages are sent

                print("Message sent successfully to topic cv-summaries!")
            else:
                print("Failed to process message with AI.")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        producer.close()

if __name__ == "__main__":
    print("Start Confluent CV Summarizer Consumer from loaded_cv_files topic.")
    main()  
    