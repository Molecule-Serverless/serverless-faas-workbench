# FROM val01:5000/python-base-image:dev-base
FROM ddnirvana/python-base-image:dev-base-3.6
RUN mkdir /env && mkdir /code
COPY daemon-base.py /env
COPY src/ /code
COPY spin  /
RUN mkdir /data
COPY SampleVideo_1280x720_10mb.mp4 /data


# Prepare deps here
RUN pip install chameleon
RUN pip install six
RUN pip install opencv-python
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6 -y
