# This program is intended to create a Chatbot that accesses a FAISS Vector database that contains uploaded CVs 
# The UI of the Chat Bot is done using the Streamlit Library.

from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAI
import os

import streamlit as st

# Read API KEY from environment
OPENAIKEY = os.getenv("OPENAI_API_KEY")
if not OPENAIKEY:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

client = OpenAI(api_key=OPENAIKEY)

index_path = "faiss_index_cvsummaries"

def query(question, chat_history):
    """
    This function does the following:
    1. Receives two parameters - 'question' - a string and 'chat_history' - a Python List of tuples containing accumulating question-answer pairs    
    2. Load the local FAISS database where the entire website is stored as Embedding vectors
    3. Create a ConversationalBufferMemory object wth 'chat_history'
    4. Create a ConversationalRetrievalChain object with the FAISS DB as the Retriever (LLM lets us create Retriever objects against data stores)
    5. Invoke the Retriever object with the Query and Chat History
    6. Returns the response
    """
    # load existing vector DB content
    embeddings = OpenAIEmbeddings()
    new_db = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

    # Initialize a ConversationalRetrievalChain
    query = ConversationalRetrievalChain.from_llm(
        llm=llm, 
        retriever=new_db.as_retriever(), 
        return_source_documents=True)
    # Invoke the Chain with
    return query({"question": question, "chat_history": chat_history})


def show_ui():
    """
    This function does the following:
    1. Implements the Streamlim UI
    2. Implements two session_state vatiables - 'messages' - to contain the accumulating Questions and Answers to be displayed on the UI and
       'chat_history' - the accumulating question-answer pairs as a List of Tuples to be served to the Retriever object as chat_history
    3. For each user query, the response is obtained by invoking the 'query' function and the chat histories are built up   
    """
    st.title("Yours Truly CVs Chatbot")    
    st.image("img/confluent-logo-300-2.png")
    st.subheader("Please enter your CV Query ")
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.chat_history = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("Enter your CV related Query: "):
        # Invoke the function with the Retriever with chat history and display responses in chat container in question-answer pairs 
        with st.spinner("Working on your query...."):     
            response = query(question=prompt, chat_history=st.session_state.chat_history)            
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.chat_message("assistant"):
                st.markdown(response["answer"])    

            # Append user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.session_state.messages.append({"role": "assistant", "content": response["answer"]})
            st.session_state.chat_history.extend([(prompt, response["answer"])])

# Program Entry.....
if __name__ == "__main__":
    show_ui() 
    