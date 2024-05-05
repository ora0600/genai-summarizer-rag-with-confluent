#!/bin/bash

confluent local services stop
confluent local destroy
echo " if you run SFTP connector on MACOS, do not forget to switch off Remote Login for the SFTP User"
rm -rf faiss_index_cvsummaries/

echo "Demo stopped and deleted"