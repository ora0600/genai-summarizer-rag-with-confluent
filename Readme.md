# Confluent CV Summarizer with RAG pattern

This is another demo app around generative AI and Confluent. Generative AI and Confluent/Apache Kafka are powerful technologies that, when combined, can revolutionize data-driven industries by enhancing real-time data processing with intelligent, automated insights. 
Our Recruitment accelerator will bring more value and faster decision-making with genAI and Confluent in the screening process. The following image shows the demo architecture
![Demo architecture](img/ConfluentGenAIPDFDocumentSummarizer.png)

The demo will use a SFTP Connector and an UI (simple streamlit APP) to load PDF Files (CVs) and generate a cv summary on a given format.
The PDF will be split into chunks and loaded as embeddings into something like a vector DB. We will use Facebook AI Similarity Search (Faiss) here (no costs). It is not a real vector DB. But for this case more than enough.
We store chunks so that we can use it later for similarity search: Show me all Java Developers (not covered yet).

The demo is very simple and should be used as a starter.
 
# prerequisites

to run this demo, please ensure that the following components are up and running.

* CP installed, I am going with Confluent Platform 7.6
* Confluent cli installed
* install SFTP Connector: `confluent-hub install confluentinc/kafka-connect-sftp:3.2.1`
* java installed, I am still on JDK 1.8
* Python 3 installed with the following python packages
```bash
pip3 install openai
pip3 install streamlit
pip3 install ast, os, json
pip3 install kafka
pip3 install -U langchain-openai
pip3 install -U langchain-openai langchain
pip3 install -U langchain-community
pip3 install -U langchain-community faiss-cpu langchain-openai
pip3 install -U langchain-openai
```

* iterm2 installed, to run the demo automatically, otherwise call each program manually. (have a look into file `01_terminals.scpt)
* Having an OpenAI Api Key. If not, create an OpenAI API Key ([https://platform.openai.com/docs/quickstart/account-setup?context=python]()) first

copy the OpenAI Key to `.env` file and complete the PDFFILE with your installation path:

```bash
cat > $PWD/.env <<EOF
export OPENAI_API_KEY=YOUR openAI Key
export PDFFILE=/your-demo-path/temp/cv.pdf
EOF
```

And finally change the paths and SFTP Setup in `jsonsftp.properties `file:

```bash
input.path=/PATH/data
error.path=/PATH/error
finished.path=/PATH/finished
...
sftp.username=sftpuser
sftp.password=PW
sftp.host=your host
sftp.port=22
```

When you run the SFTP Connector on your Mac, you just need to add a new user, and enable Remote Login. (Switch it off, after running the Demo)

# AI Demo Confluent CV Summarizer

We will run a demo with the possibility to upload a CV on different ways:

* via UI: In this case we will take the CV via UI file-uploader, split the document into chunks and add them into a kind of vector DB (here local FAISS) and generate the summary and put the summary into topic cv-summaries
* or via SFTP Connector to just download the file into the topic loaded-cv-files, a second client consumer will consume from topic loaded-cv-files split the document chunks and add them into a kind of vector DB (here local FAISS) and generate the summary and put the summary into topic cv-summaries

Start the Demo by executing:

```bash
./00_start_ai_demo.sh
```

A terminal Window will opened automatically and show the following window sessions:
![Demo terminals](img/terminals.png)

* First: Session to copy files to data directory, from there the SFTP Connector will take it (Names are unique, a file with the same name, will be processed once), Press ENTER to load each CV once by once.
* Second: Start UI. Download a CV by pressing the button via [UI](http://localhost:8501/), the file will then be processed by AI and the results are shown as print-outs. 
* Third: genAI CV-Summarizer Consumer reading from Topic `loaded-cv-files` (1.Step) and doing genAI CV-Summary generation and produce to topic `cv-summaries`
* Fourth: simple consumer from topic `cv-summaries` to show again the generated content which was stored in the mentioned topic `cv-summaries`

The UI Demo looks like the next image, and shows immediately after file-loading the result.
![Demo terminals](img/demo_ui.png)

To work with UI go to [http://localhost:8501/](http://localhost:8501/)

Play around and have fun (-:

# Delete Demo

run the following command:

```bash
./02_stop_and_destroy_ai_demo.sh
```

Don't forget to switch off, Remote Login.