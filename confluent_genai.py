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
OPENAIKEY = os.getenv("OPENAI_API_KEY")
if not OPENAIKEY:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

client = OpenAI(api_key=OPENAIKEY)


def load_and_process_with_ai(pdf_file):
    try:
        # Load file
        text=""
        #PYPDFLoader loads a list of PDF Document objects
        loader = PyPDFLoader(pdf_file)
        documents = loader.load()
        for page in documents:
            text += page.page_content.replace('\t', ' ')
            
        text_splitter = CharacterTextSplitter(
                separator="\n",
                chunk_size=1000,
                chunk_overlap=50
            )
        
        docs = text_splitter.split_documents(documents=documents)
        embeddings = OpenAIEmbeddings()
        vectorstore = FAISS.from_documents(docs, embeddings)
        
        # Save and load FAISS index securely
        index_path = "faiss_index_cvsummaries"
        vectorstore.save_local(index_path)
        
        new_vectorstore = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
        qa = RetrievalQA.from_chain_type(
            llm=OpenAI(api_key=OPENAIKEY),
            chain_type="stuff",
            retriever=new_vectorstore.as_retriever()
        )
        
        prompt = ("Give me a summary of the uploaded CV in 3 sentences. "
                  "What is the person's Name, Email, Key Skills, Last Company, and Experience Summary? "
                  "Please respond in JSON format like this: "
                  "{Name: 'Max Mustermann', Email: 'max@mustermann.de', Skills: 'dancing', Last Company: 'BSR', "
                  "Experience Summary: 'nice, strong, good dancer'}")
        response = qa.invoke(prompt)

        # Safely parse JSON response
        parsed_response = ast.literal_eval(str(response))
        result_value = parsed_response.get('result', '')
                
        return result_value
    except Exception as e:
        print(f"Error processing message with AI: {e}")
        return None
    

    