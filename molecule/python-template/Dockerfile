# FROM val01:5000/python-base-image:dev-base
FROM ddnirvana/python-base-image:dev-base-3.6
RUN mkdir /env
COPY src/setup.py /env

COPY src/ol.c /env

RUN cd /env && python3 setup.py build_ext --inplace && mv ol.*.so /env/ol.so

COPY src/daemon.py /env
COPY src/daemon-loop.py /env

# Prepare deps here
RUN pip install six chameleon
RUN pip install opencv-python
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6 -y
RUN pip install numpy
