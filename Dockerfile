FROM osrf/ros:melodic-desktop-bionic
LABEL maintainer="gauthiermartin86@gmail.com"
LABEL description="A ROS with diffrent utility script"

# *********************************************
# Declaring environements variables
# Never prompts the user for choices on installation/configuration of packages
ENV DEBIAN_FRONTEND noninteractive
ENV TERM linux

# Specific
# ENV SONIA_USER=sonia
ENV SONIA_HOME=/home/root
ENV BAGS_FOLDER=${SONIA_HOME}/bags
ENV IMAGES_FOLDER=${SONIA_HOME}/images
# *********************************************
# RUN useradd -ms /bin/bash -d ${SONIA_HOME} ${SONIA_USER} -G root

# *********************************************
# Update OS and install required dependencies
RUN apt-get update -yqq \
    && apt-get upgrade -yqq \
    && apt-get install -yqq --no-install-recommends \
    python-pip \
    && pip install setuptools wheel

# Install python required libraries
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

# *********************************************
# Copy required scripts and creating folders
ADD app ${SONIA_HOME}/
RUN chown -R ${SONIA_USER}: ${SONIA_HOME}
RUN mkdir -p ${BAGS_FOLDER} ${IMAGES_FOLDER}
# *********************************************
RUN ls -lat /home/
COPY script/entrypoint.sh /entrypoint.sh

WORKDIR ${SONIA_HOME}
ENTRYPOINT [ "/entrypoint.sh" ]
