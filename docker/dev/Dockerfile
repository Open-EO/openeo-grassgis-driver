FROM mundialis/openeo-grassgis-driver:latest as base

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=openeo_grass_gis_driver.main
ENV FLASK_ENV=development
ENV FLASK_DEBUG=1
ENV DEFAULT_CONFIG_PATH=/src/openeo_grass_gis_driver/config

RUN apk add make git

RUN pip3 uninstall openeo-grass-gis-driver -y

COPY . /src/openeo_grass_gis_driver/
COPY config/sample.ini /src/openeo_grass_gis_driver/config/config.ini

WORKDIR /src/openeo_grass_gis_driver/
RUN pip3 install -e .

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "openeo_grass_gis_driver.main"]
