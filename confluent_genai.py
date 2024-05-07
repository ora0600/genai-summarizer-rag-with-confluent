# GenAI Lib for Demo
import os
import ast
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_openai import OpenAI

# Read API KEY from environment
OPENAIKEY = os.environ["OPENAI_API_KEY"]
client = OpenAI(api_key=OPENAIKEY)


def load_and_process_with_ai(pdf_file):
    try:
        # Load file
        text=""
        #PYPDFLoader loads a list of PDF Document objects
        loader=PyPDFLoader(pdf_file)
        documents = loader.load()
        for page in documents:
            text+=page.page_content
            text= text.replace('\t', ' ')
        #splits a long document into smaller chunks that can fit into the LLM's 
        #model's context window
        text_splitter = CharacterTextSplitter(
                separator="\n",
                chunk_size=1000,
                chunk_overlap=50
            )
        #create_documents() create documents from a list of texts
        docs = text_splitter.split_documents(documents=documents)
        embeddings = OpenAIEmbeddings()
        vectorstore = FAISS.from_documents(docs, embeddings)
        vectorstore.save_local("faiss_index_cvsummaries")

        new_vectorstore = FAISS.load_local("faiss_index_cvsummaries", embeddings, allow_dangerous_deserialization=True)
        qa = RetrievalQA.from_chain_type(
            llm=OpenAI(), chain_type="stuff", retriever=new_vectorstore.as_retriever()
        )
        res = qa.invoke("Give me a summary of the uploaded CV in 3 sentences. What is the persons Name, Email, Key Skills, Last Company, Experience Summary. Can you please response in a json format like this: {  Name: Max Mustermann, Email: max@mustermann.de, Skills: tanzen, Last Company: BSR, Experience Summary: Is is nice, strong, and a good dancer}")
        response = str(res) 
        parsed_response = ast.literal_eval(response)
        # Access the 'result' key from the parsed response
        result_value = parsed_response['result']
        return result_value
    except Exception as e:
        print(f"Error processing message with AI: {e}")
        return None
    

    