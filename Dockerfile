FROM ubuntu:18.04
RUN useradd -m -d /home/user -s /bin/bash -u 1000 user
RUN apt-get update
RUN apt-get install -y --no-install-recommends python3-pip ruby ruby-dev
RUN apt-get install -y --no-install-recommends supervisor 
RUN gem install goliath -v 1.0.6

COPY ./app /app

COPY ./util/supervisord.conf /etc/supervisor/conf.d/
COPY ./util/haproxy /home/haproxy/
COPY ./util/haproxy.cfg /home/haproxy/

RUN pip3 install -r /app/requirements.txt

RUN useradd -UM app \
    && useradd -UMr haproxy

RUN chown haproxy:haproxy /home/haproxy/ /home/haproxy/haproxy.cfg /home/haproxy/haproxy

EXPOSE 8080
WORKDIR /app
RUN python3 manage.py makemigrations
RUN python3 manage.py migrate
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
