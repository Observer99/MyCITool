FROM frolvlad/alpine-python3
MAINTAINER Michael Haskelsky
LABEL version="1.0"

COPY cherrypy-hello-world.py cherrypy-hello-world.py
COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

EXPOSE 8080

ENTRYPOINT ["python3", "cherrypy-hello-world.py"]
