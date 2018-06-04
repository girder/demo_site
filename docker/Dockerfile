FROM ubuntu:18.04

# the below incantation makes tzdata non-interactive installation work
ENV DEBIAN_FRONTEND noninteractive
ENV DEBCONF_NONINTERACTIVE_SEEN true
RUN echo "tzdata tzdata/Areas select America" > /tmp/preseed.txt; \
    echo "tzdata tzdata/Zones/America select New York" >> /tmp/preseed.txt; \
    debconf-set-selections /tmp/preseed.txt && \
    apt-get update && \
    apt-get install -y tzdata
RUN apt-get install -y \
    software-properties-common build-essential cmake git python-dev python-pip \
    libopencv-dev python-opencv libinsighttoolkit4-dev
RUN pip install click itk

# Build Timelapse-OpticalFlow
RUN git clone https://github.com/KitwareMedical/TimeLapse-OpticalFlow.git && \
    mkdir -p _build && cd _build && cmake ../TimeLapse-OpticalFlow && make -j4

COPY ./run.py /run.py

ENTRYPOINT ["python", "/run.py"]
