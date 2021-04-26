# FROM val01:5000/python-base-image:dev-base
FROM ddnirvana/python-base-image:dev-base-3.6
RUN mkdir /env
COPY src/setup.py /env

COPY src/ol.c /env

RUN cd /env && python3 setup.py build_ext --inplace && mv ol.*.so /env/ol.so

COPY src/daemon.py /env
COPY src/daemon-loop.py /env

RUN pip install six chameleon
