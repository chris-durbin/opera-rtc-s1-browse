FROM ghcr.io/lambgeo/lambda-gdal:3.8-python3.11

ENV PACKAGE_PREFIX=/var/deployment_package

RUN yum install -y git zip

# Install python package and dependencies
COPY . .
RUN python -m pip install . -t $PACKAGE_PREFIX

# Reduce size of the C libs
RUN cd $PREFIX && find lib -name \*.so\* -exec strip {} \;

# Create package.zip
# Archive python code (installed in $PACKAGE_PREFIX/)
RUN cd $PACKAGE_PREFIX && zip -r9q /tmp/package.zip *

# Archive GDAL libs (in $PREFIX/lib $PREFIX/bin $PREFIX/share)
RUN cd $PREFIX && zip -r9q --symlinks /tmp/package.zip lib/*.so* share
RUN cd $PREFIX && zip -r9q --symlinks /tmp/package.zip bin/gdal* bin/ogr* bin/geos* bin/nearblack
