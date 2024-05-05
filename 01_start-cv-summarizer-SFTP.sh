#!/bin/bash
# Set title
export PROMPT_COMMAND='echo -ne "\033]0;Start Consumer from Topic loaded-cv-files with AI output generation:\007"'
echo -e "\033];Start Consumer from Topic loaded-cv-files with AI output generation:\007"

# Consume raw events Terminal 1
echo "Start Consumer from Topic loaded-cv-files with AI output generation:: "
source .env
python3 cv-summary-consumerSFTP.py -W