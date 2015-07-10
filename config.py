# ------------------------------------------------------------------------------
# Config
# ------------------------------------------------------------------------------

import os

class BaseConfig():
    
    basedir = os.path.abspath(os.path.dirname(__file__))
    # Should the application be in debug mode?
    DEBUG = os.getenv('DEBUG', True)

    # Host, port
    #SERVER_NAME = '%s:%s' % (os.getenv("HOSTNAME", "0.0.0.0"), os.getenv("PORT", 8080))

    # Database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    
class ProductionConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')