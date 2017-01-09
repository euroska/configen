# -*- coding: utf-8 -*-
from __future__ import print_function
import os
from sqlalchemy import create_engine, text
from jinja2 import Environment, FileSystemLoader

class Configen(object):

    def __init__(self, config):
        self.config = config

        self.test()

        self.jinja = Environment(
            loader=FileSystemLoader(config.get('templateDir'))
        )

        self._connections = {}

    def getConnection(self, connection):
        if connection in self._connections:
            return self._connections[connection]

        if connection in self.config.get('connections', {}):
            engine = create_engine(self.config['connections'][connection])
            self._connections[connection] = engine
            return engine

        raise NameError('Connection does not exists')


    def getQuery(self, connection, query):
        if not connection or not query:
            return None

        c = self.getConnection(connection)
        return c.execute(
            text(query),
            self.config.get('environment')
        )

    def run(self):
        '''
        Process config
        '''

        for rule in self.config.get('rules', []):
            print("Processing %s" % rule.get('name'))

            template = self.jinja.get_template(
                rule.get('template'),
                globals=self.config.get('environment', {})
            )

            query = None

            destination = rule.get('dest')

            folder = os.path.dirname(destination)
            if not os.path.exists(folder):
                os.makedirs(folder)

            file = open(rule.get('dest'), 'w')
            file.write(template.render(
                query=self.getQuery(
                    rule.get('connection', 'main'),
                    rule.get('query'),
                )
            ))
            file.close()

            try:
                mode = rule.get('mode')
                if mode is not None:
                    os.chmod(destination, rule.get('mode'))

                user = rule.get('user', -1)
                group = rule.get('group', -1)

                if user > 0 or group > 0:
                    os.chown(destination, user, group)
            except Exception as e:
                print(e)

        self.clean()

    def test(self):
        '''
        Test configuration
        '''
        pass

    def clean(self):
        '''
        Cleanup connections
        '''
        pass
