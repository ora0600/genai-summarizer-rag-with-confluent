from kafka import KafkaProducer
import json
import streamlit as st
import confluent_genai

# Define the topic name
topic = 'cv-summaries'

# Configure Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],  # List of Kafka broker addresses
    value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Serializer for the message data
)

def main():
    st.title("Confluent CV Summary Generator")
    uploaded_file = st.file_uploader("Select CV", type=["pdf"])
    text = ""
    if uploaded_file is not None:
        # extract file extension
        file_extension = uploaded_file.name.split('.')[-1]
        st.write("File Details:")
        st.write(f"File Name: {uploaded_file.name}")
        st.write(f"File Type: {file_extension}")
        text = confluent_genai.load_and_process_with_ai(uploaded_file.name)
        print("Show loading document:")
        print(text)
        st.write("Resume Summary:")
        st.text_area("Text", text, height=400)
        if text:
            # Produce to Kafka
            producer.send(topic, text)
            # Wait for all messages to be sent
            producer.flush()
            producer.close()
        
if __name__ == "__main__":
    print("Start Confluent CV Summarizer")
    main()

