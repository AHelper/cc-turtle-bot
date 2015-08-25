FROM fedora:22

RUN dnf install python python-setuptools -y
RUN dnf install python-pip -y
RUN pip install tornado

# Use last
ADD files /opt
WORKDIR /opt
RUN ls
RUN python setup.py install
