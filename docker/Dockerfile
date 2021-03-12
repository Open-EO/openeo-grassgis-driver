FROM alpine:3.13 as common
RUN apk add --no-cache python3 py3-gdal
RUN python3 -m ensurepip && pip3 install --upgrade pip wheel

FROM common as build
RUN apk add git
RUN pip3 install setuptools
COPY . /src/openeo_grass_gis_driver
WORKDIR /src/openeo_grass_gis_driver
RUN python3 setup.py sdist bdist_wheel -d /build

FROM common as install
COPY --from=build /build/*.whl /build/
COPY requirements.txt /src/requirements.txt
RUN sed -i 's+Sphinx+#Sphinx+g' /src/requirements.txt
RUN pip3 install -r /src/requirements.txt
RUN pip3 install /build/*

FROM install as test
RUN apk add make git
COPY --from=build /src/openeo_grass_gis_driver /src/openeo_grass_gis_driver
WORKDIR /src/openeo_grass_gis_driver
RUN make test

FROM install as app
ENV GDAL_CACHEMAX="25%"
CMD ["gunicorn", "-b", "0.0.0.0:5000", "openeo_grass_gis_driver.main:flask_app"]
EXPOSE 5000
