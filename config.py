import os


class Config(object):
    DATABASE_NAME = 'nyvolako'
    DATABASE_CREDENTIALS = 'nyvolako:nyvolako'
    DATABASE_HOST_PORT = 'localhost:5432'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        "postgresql://{}@{}/{}".format(DATABASE_CREDENTIALS, DATABASE_HOST_PORT, DATABASE_NAME)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # https://stackoverflow.com/questions/55457069/how-to-fix-operationalerror-psycopg2-operationalerror-server-closed-the-conn
    SQLALCHEMY_ENGINE_OPTIONS = {'pool_pre_ping': True, 'pool_recycle': 300}
    TRACE_MODE = os.environ.get('TRACE_MODE') or False


class ConfigTest(object):
    DATABASE_NAME = 'nyvolako_test'
    DATABASE_CREDENTIALS = 'nyvolako:nyvolako'
    DATABASE_HOST_PORT = 'localhost:5432'
    SQLALCHEMY_DATABASE_URI = "postgresql://{}@{}/{}".format(DATABASE_CREDENTIALS, DATABASE_HOST_PORT, DATABASE_NAME)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TRACE_MODE = True
