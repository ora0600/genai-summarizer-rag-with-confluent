#/bin/bash
# Set title
export PROMPT_COMMAND='echo -ne "\033]0;Copy CV-files to SFTP Connector Directory\007"'
echo -e "\033];Copy CV-files to SFTP Connector Directory\007"

# Produce to support-ticket topic Terminal 1
echo "Copy CV-files to SFTP Connector Directory: "
echo "copy CV_peter_pan.pdf into Data Dir: Press enter to copy..."
read a
cp CV_peter_pan.pdf data/CV_peter_pan.pdf
echo "CV_peter_pan.pdf copied to data/ now Connector will process."
echo "***************************************************************"
echo "copy cv_donald_duck.pdf into data/ Dir: Press enter to copy..."
read b
cp cv_donald_duck.pdf data/cv_donald_duck.pdf
echo "cv_donald_duck.pdf copied to data/ now Connector will process."
echo "***************************************************************"
echo "copy cv_kalle.pdf into Data Dir: Press enter to copy..."
read c
cp cv_kalle.pdf data/cv_kalle.pdf
echo "cv_kalle.pdf copied to data/ now Connector will process."
echo "***************************************************************"

echo "no more CV files"