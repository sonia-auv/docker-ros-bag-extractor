FROM osrf/ros:melodic-desktop-bionic
LABEL maintainer="gauthiermartin86@gmail.com"
LABEL description="A ROS with diffrent utility script"

# *********************************************
# Declaring environements variables
# Never prompts the user for choices on installation/configuration of packages
ENV DEBIAN_FRONTEND noninteractive
ENV TERM linux

# Specific
ENV SONIA_USER=sonia
ENV SONIA_HOME=/home/sonia
ENV BAGS_FOLDER=${SONIA_HOME}/bags
ENV IMAGES_FOLDER=${SONIA_HOME}/images
# *********************************************
RUN useradd -ms /bin/bash -d ${SONIA_HOME} ${SONIA_USER}

# *********************************************
# Copy required scripts and creating folders
ADD app ${SONIA_HOME}/
RUN mkdir -p ${BAGS_FOLDER} ${IMAGES_FOLDER}
RUN chown -R ${SONIA_USER}: ${SONIA_HOME}
# *********************************************
# *********************************************
USER ${SONIA_USER}
WORKDIR ${SONIA_HOME}
