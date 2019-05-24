FROM frolvlad/alpine-python3
MAINTAINER Michael Haskelsky
LABEL version="1.0"

COPY requirements.txt requirements.txt 
RUN pip3 install -r requirements.txt

COPY cherrypy-hello-world.py cherrypy-hello-world.py
ENTRYPOINT ["python3", "cherrypy-hello-world.py"]
