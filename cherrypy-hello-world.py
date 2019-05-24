#!/usr/bin/env python3

import cherrypy

class HelloWorld(object):
    @cherrypy.expose
    def index(self):
        return "Hello world!"

cherrypy.config.update({'server.socket_host': '0.0.0.0',
                        'server.socket_port': 8080,
                       })

cherrypy.quickstart(HelloWorld())

