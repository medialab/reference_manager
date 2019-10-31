FROM python:2.7-alpine

COPY . /reference_manager
WORKDIR /reference_manager

ENV PIP_CACHE /tmp/pipcache
ENV PYTHONPATH $PYTHONPATH:/reference_manager

RUN apk --update add gcc git musl-dev libxml2-dev libxslt-dev libffi-dev openssl-dev \
    && pip install --cache-dir=$PIP_CACHE -U setuptools pip \
    && pip install --cache-dir=$PIP_CACHE -r requirements_frozen.txt \
    && pip install --cache-dir=$PIP_CACHE git+https://github.com/medialab/txjsonrpc.git@adbcdc91ce0a79226d3bd6cc4b65a717212acfe1 \
    && pip install --cache-dir=$PIP_CACHE git+https://github.com/asl2/PyZ3950.git@c2282c73182cef2beca0f65b1eb7699c9b24512e \
    && rm -rf $PIP_CACHE \
    && rm -rf /tmp/pip-req-build* \
    && rm /var/cache/apk/*

RUN cp conf/config.docker.json conf/config.json

RUN mkdir -p /logs

ENTRYPOINT ["/reference_manager/entrypoint.sh"]
