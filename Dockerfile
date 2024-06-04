FROM ghcr.io/lambgeo/lambda-gdal:3.8-python3.11

ENV \
  GDAL_DATA=/opt/share/gdal \
  PROJ_LIB=/opt/share/proj \
  GDAL_CONFIG=/opt/bin/gdal-config \
  GEOS_CONFIG=/opt/bin/geos-config \
  PATH=/opt/bin:$PATH

ENV PACKAGE_PREFIX=/var/deployment_package

COPY src ${PACKAGE_PREFIX}

COPY requirements.txt /tmp/requirements.txt
RUN python -m pip install -r /tmp/requirements.txt -t $PACKAGE_PREFIX
