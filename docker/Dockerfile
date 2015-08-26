FROM fedora:22

RUN dnf install python python-setuptools -y
RUN dnf install python-pip -y
RUN pip install tornado pyyaml

# Use last
WORKDIR /opt
ADD files /opt
RUN python setup.py install
