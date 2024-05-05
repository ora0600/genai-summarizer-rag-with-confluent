#!/bin/bash
# prereqs
# CP installed, i use 7.6
# java installed at least 1.8
# Python 3 installed with the following python packages
# iterm2 installed
# Having an Open AI Api Key

pwd > basedir
export BASEDIR=$(cat basedir)

source .env

echo "Start AI Demo: Confluent CV Summarizer"

echo "Start Confluent, running 7.6.0"
confluent local services start
# Install SFTP Connector
#confluent-hub install confluentinc/kafka-connect-sftp:3.2.1

# Create topic for the PDf Files (CV)
kafka-topics --bootstrap-server localhost:9092 --create --partitions 1 --replication-factor 1 --topic loaded-cv-files
# Create topic for the CV-Summaray
kafka-topics --bootstrap-server localhost:9092 --create --partitions 1 --replication-factor 1 --topic cv-summaries

# Before starting connector you need to enable your Mac to act as a SFTP Server.
# Create a new user and give him standard role and File Sharing and enable remote login (search for file Sharing in System Settings)
# Allow writing to these dirs
chmod ugo+w data/
chmod ugo+w error/
chmod ugo+w finished/

# Start connector
confluent local services connect connector load BinaryCVSFTP-Connector --config jsonsftp.properties
# Status Connector
confluent local services connect connector status BinaryCVSFTP-Connector

# Start iterm Demo
# Start Terminal
echo ""
echo "Start Clients from demo...."
open -a iterm
sleep 10
osascript 01_terminals.scpt $BASEDIR

echo "AI Demo started"