import os
from flask.ext.script import Manager, Server
from flask.ext.migrate import MigrateCommand

from app import app

# Create manager
manager = Manager(app)

# Add migrate
manager.add_command('db', MigrateCommand)

# Set server commands
server = Server (host=os.getenv("HOSTNAME", "0.0.0.0"), port=os.getenv("PORT", 8080))
manager.add_command("runserver", server)

@manager.command
def hello():
    print "hello"

if __name__ == "__main__":
    manager.run()