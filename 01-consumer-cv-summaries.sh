#!/bin/bash
# Set title
export PROMPT_COMMAND='echo -ne "\033]0;Consume from cv-summaries topic\007"'
echo -e "\033];Consume from cv-summaries topic\007"

# Consume ai generated CV Summary
echo "Consume from cv-summaries topic: "
kafka-console-consumer --bootstrap-server localhost:9092 --topic cv-summaries