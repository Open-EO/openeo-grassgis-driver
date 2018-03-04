# Use standard ubuntu 16.04
FROM ubuntu:16.04

EXPOSE 5000

RUN apt update && apt upgrade -y && \
    apt update && apt install --no-install-recommends --no-install-suggests \
    git \
    build-essential \
    flex \
    make \
    bison \
    gcc \
    libgcc1 \
    g++ \
    python3.5 \
    python3.5-dev \
    python3-pip -y  && \
    apt-get clean && \
    apt-get autoremove

# Set the working directory to /src
WORKDIR /src

# Clone the GRaaS software
RUN git clone https://bitbucket.org/huhabla/openeo_core.git openeo_core

WORKDIR /src/openeo_core
RUN pip3 install --upgrade pip &&  \
    pip3 install -U setuptools && \
    pip3 install wheel && \
    pip3 install -r requirements.txt && \
    python3.5 setup.py install

WORKDIR /tmp/blaupause

WORKDIR /src

RUN git clone https://bitbucket.org/huhabla/graas_openeo_core_wrapper.git graas_openeo_core_wrapper

WORKDIR /src/graas_openeo_core_wrapper
RUN pip3 install -r requirements.txt && \
    python3.5 setup.py install

CMD python3.5 -m graas_openeo_core_wrapper.main
