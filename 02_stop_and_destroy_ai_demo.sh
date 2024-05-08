#!/bin/bash

confluent local services stop
confluent local destroy
echo " if you run SFTP connector on MACOS, do not forget to switch off Remote Login for the SFTP User"
# Delete files
rm basedir
rm -rf faiss_index_cvsummaries/
rm data/*.pdf
rm error/*.pdf
rm finished/*.pdf
echo "Demo stopped and deleted"