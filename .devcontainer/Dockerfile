ARG BASE_IMAGE
FROM $BASE_IMAGE

WORKDIR /
ENV DEBIAN_FRONTEND=noninteractive

# Install esstinal Ubuntu packages
RUN apt-get update && apt-get install --no-install-recommends -y \
    software-properties-common \
    apt-utils \
    sudo \
    build-essential \
    git \
    curl \
    wget \
    zip \
    unzip \
    pkg-config \
    libgl-dev \
    libblas-dev \
    liblapack-dev \
    python3-tk \
    python3-wheel \
    libhdf5-dev \
    python3.8 \
    python3.8-dev \
    python3.8-distutils \
    swig \
    apt-transport-https \
    lsb-release \
    bash-completion \
    ca-certificates &&\
    apt-get clean &&\
    ln -s /usr/bin/python3.8 /usr/local/bin/python &&\
    ln -s /usr/bin/python3.8 /usr/local/bin/python3 &&\
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py &&\
    python3 get-pip.py &&\
    rm get-pip.py 

# pip dependencies
RUN pip3 install --upgrade pip &&\
    pip3 install dtlpy \
                 numpy
