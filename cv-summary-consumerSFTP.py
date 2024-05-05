from kafka import KafkaConsumer
from kafka import KafkaProducer
import os
import ast
import json
import PyPDF2
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_openai import OpenAI


# REad API KEY from environment
OPENAIKEY = os.environ["OPENAI_API_KEY"]
pdffile  = os.environ["PDFFILE"]
client = OpenAI(api_key=OPENAIKEY)
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
def load_and_process_with_ai(message):
    try:
        # Load file
        loader = PyPDFLoader(message)
        documents = loader.load()
        text_splitter = CharacterTextSplitter(
            chunk_size=1000, chunk_overlap=30, separator="\n"
            )
        docs = text_splitter.split_documents(documents=documents)
        embeddings = OpenAIEmbeddings()
        vectorstore = FAISS.from_documents(docs, embeddings)
        vectorstore.save_local("faiss_index_cvsummaries")

        new_vectorstore = FAISS.load_local("faiss_index_cvsummaries", embeddings, allow_dangerous_deserialization=True)
        qa = RetrievalQA.from_chain_type(
            llm=OpenAI(), chain_type="stuff", retriever=new_vectorstore.as_retriever()
        )
        res = qa.invoke("Give me a summary of the uploaded CV in 3 sentences. What is the persons Name, Email, Key Skills, Last Company, Experience Summary. Can you please response in a json format like this: {  Name: Max Mustermann, Email: max@mustermann.de, Skills: tanzen, Last Company: BSR, Experience Summary: he is nice, strong, and a good dancer}")
        response = str(res) 
        parsed_response = ast.literal_eval(response)
        # Access the 'result' key from the parsed response
        result_value = parsed_response['result']
        return result_value
    except Exception as e:
        print(f"Error processing message with AI: {e}")
        return None

for message in consumer:
        # Read Bytes Data from Kafka
        msg_value = message.value
        # Transform Bytes into a temp cv.pdf file
        with open(pdffile, 'wb') as file: 
            file.write(msg_value) 
        print(f"**** MESSAGE FROM SFTP Server ****")
        print(f"Received message:")
        # ai_output = load_and_process_with_ai(msg_value)
        ai_output = load_and_process_with_ai(pdffile)
        if ai_output:
            print(f"**** CV-Summary ****")
            print(f"AI processed output: {ai_output}")
            # Send a message
            message = ai_output
            print(message)
            # Transform into JSON
            # json_data_decoding = json.loads(message)
            #name=json_data_decoding['Name']
            #email=json_data_decoding['Email']
            #skills=json_data_decoding['Skills']
            #last_company=json_data_decoding['Last Company']
            #experience=json_data_decoding['Experience Summary']
            # producer.send(topic, json_data_decoding)
            producer.send(topic, message)
            # Wait for all messages to be sent
            #producer.flush()
            print("Message sent successfully to topic cv-summaries!")
        else:
            print("Failed to process message with AI.")
# Optionally, close the producer
producer.close()
    
    
    