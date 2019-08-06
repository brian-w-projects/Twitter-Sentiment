

class Config:
    pass

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = False
    SECRET_KEY = 'asdlfasdflkjsdf'


class DeploymentConfig(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS = False


config = {
    'development': DevelopmentConfig,
    'deployment': DeploymentConfig
}