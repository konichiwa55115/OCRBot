#Thank you LazyDeveloper for helping me in this journey !
#Must Subscribe On YouTube @LazyDeveloperr
# Python Based Docker
# Python Based Docker
FROM python:3.9-buster

# Installing Packages
RUN apt update && apt upgrade -y
RUN apt install git curl python3-pip -y
RUN apt install dos2unix
RUN apt install tesseract-ocr -y

# Updating Pip Packages
RUN pip3 install -U pip

# Copying Requirements
COPY requirements.txt /requirements.txt

# Installing Requirements
RUN cd /
RUN pip3 install -U -r requirements.txt
RUN mkdir /LazyDeveloper
WORKDIR /LazyDeveloper
COPY start.sh /start.sh

# Running MessageSearchBot
RUN dos2unix /start.sh
CMD ["/bin/bash", "/start.sh"]
