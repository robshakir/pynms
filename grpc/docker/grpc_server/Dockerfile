FROM debian:jessie
ENV DEBIAN_FRONTEND noninteractive

RUN echo "deb http://http.debian.net/debian jessie-backports main" > /etc/apt/sources.list.d/jessie_backports.list
RUN apt-get -y --force-yes update
RUN apt-get install -y supervisor python-pip python2.7 zlib1g-dev libgrpc-dev python-dev libxml2-dev libxslt1-dev python-virtualenv
RUN pip install --upgrade pip
RUN mkdir -p /opt
RUN virtualenv /opt/virtualenv

COPY supervisord.conf /etc/supervisord.conf
COPY ./PyNMSGRPC-0.0.1-py2-none-any.whl /tmp
COPY ./PyNMSYANGExamples-0.0.1-py2-none-any.whl /tmp
RUN /opt/virtualenv/bin/pip install /tmp/PyNMSGRPC-0.0.1-py2-none-any.whl
RUN /opt/virtualenv/bin/pip install /tmp/PyNMSYANGExamples-0.0.1-py2-none-any.whl
RUN rm /tmp/*.whl
RUN /opt/virtualenv/bin/pip install pyaml
COPY server /opt/pynms_server

EXPOSE 50051
#CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]
CMD ["/bin/sleep", "86400"]

