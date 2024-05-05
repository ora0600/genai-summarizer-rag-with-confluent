#!/bin/bash
# Set title
export PROMPT_COMMAND='echo -ne "\033]0;Start cv-summarizer Client UI\007"'
echo -e "\033];Start cv-summarizer Client UI\007"

# Consume raw events Terminal 1
echo "Start cv-summarizer Client UI: "
echop "open URL http://localhost:8501/"
source .env
streamlit run cv-summary-producer.py