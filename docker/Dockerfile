# Use standard ubuntu 16.04
FROM ubuntu:18.04

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
    libgdal-dev \
    python3 \
    python3-dev \
    python3-pip -y  && \
    apt-get clean && \
    apt-get autoremove

# Set the working directory to /src
WORKDIR /src

RUN git clone https://github.com/Open-EO/openeo-grassgis-driver.git openeo_grass_gis_driver

WORKDIR /src/openeo_grass_gis_driver
RUN git checkout "openeo-api-0.3.0"

RUN pip3 install --upgrade pip
RUN pip3 install -U setuptools
RUN pip3 install wheel
RUN pip3 install -r requirements.txt

ENV SETUPTOOLS_SCM_PRETEND_VERSION=0.0.1
ENV SETUPTOOLS_SCM_DEBUG=1
RUN make install
RUN make test

CMD python3 -m openeo_grass_gis_driver.main
