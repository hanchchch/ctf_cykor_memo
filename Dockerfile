FROM ubuntu:18.04
RUN useradd -m -d /home/user -s /bin/bash -u 1000 user
RUN apt-get update
RUN apt-get install -y --no-install-recommends python3-pip

COPY . /app

RUN pip3 install -r /app/requirements.txt

EXPOSE 8000
WORKDIR /app
ENTRYPOINT [ "gunicorn" ]
CMD ["cykor_memo.wsgi"]