FROM python:3.12.12-bookworm
MAINTAINER Jamie Wolf

# work around TZ data prompting for interaction
ENV TZ=America/Toronto
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y \
    build-essential \
    ca-certificates \
    gcc \
    make \
    cifs-utils \
    git

RUN apt-get install -y \
    libpq5 \
    libpq-dev \
    python3-dev \
    libssl-dev \
    openssl \
    libxml2-dev \
    libxslt1-dev \
    tzdata\
    libzbar0

# Create a folder to host the main project files
RUN mkdir -p /opt/roguestudio/voidseekerbot
RUN mkdir -p /opt/voidseekerLog
RUN mkdir -p /opt/voidseekerStore
WORKDIR /opt/roguestudio/voidseekerbot

# Copy the project files to the image
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt


# Copy bot to docker
COPY libvoidseeker libvoidseeker
COPY docker/startup.sh ./startup.sh
COPY migrations migrations
COPY voidseeker.py ./

RUN chmod +x startup.sh

CMD ["/opt/roguestudio/voidseekerbot/startup.sh"]