FROM fedora:22

RUN dnf install python python-setuptools -y

# Use last
ADD files /opt
WORKDIR /opt
RUN ls
RUN python setup.py install
