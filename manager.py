from __future__ import absolute_import

from flask_script import Manager, Server
from coral.app import create_app


manager = Manager(create_app)
manager.add_command('runserver', Server(host='0.0.0.0', port=8888))


if __name__ == '__main__':
    manager.run()