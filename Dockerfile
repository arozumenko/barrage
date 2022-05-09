FROM python:3.8-alpine

RUN apk update && apk add --no-cache supervisor docker docker-compose git bash
WORKDIR /tmp
RUN cd /tmp
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
COPY static /tmp/static
COPY templates /tmp/templates
COPY app.py /tmp/app.py
COPY main.py /tmp/main.py
COPY start.sh /tmp/start.sh
RUN chmod +x /tmp/start.sh
EXPOSE 5000

ENTRYPOINT ["/tmp/start.sh"]