FROM ubuntu:18.04
RUN apt-get update
RUN apt-get install -y --no-install-recommends python3-pip python3-wheel\
    && apt-get install -y --no-install-recommends supervisor 

COPY ./app /app

COPY ./util/requirements.txt /app/
COPY ./util/supervisord.conf /etc/supervisor/conf.d/
COPY ./util/haproxy /home/haproxy/
COPY ./util/haproxy.cfg /home/haproxy/
COPY ./util/visitor.py /home/visitor/visitor.py
COPY ./util/init_db.py /app/init_db.py

RUN pip3 install -U pip setuptools
RUN pip install -r /app/requirements.txt

RUN useradd -UM app \
    && useradd -UMr haproxy \
    && useradd -UMr visitor

RUN chown haproxy:haproxy /home/haproxy/ /home/haproxy/haproxy.cfg /home/haproxy/haproxy
RUN chown visitor:visitor /home/visitor/ /home/visitor/visitor.py

EXPOSE 8080
WORKDIR /app
RUN python3 manage.py makemigrations
RUN python3 manage.py migrate
RUN python3 init_db.py
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
