class Development(object):
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'postgres://user:pass@localhost/my_database'


class Testing(object):
    DEBUG = False

    SQLALCHEMY_DATABASE_URI = 'postgres://user:pass@test/my_database'


class Production(object):
    DEBUG = False

    SQLALCHEMY_DATABASE_URI = 'postgres://user:pass@prod/my_database'
