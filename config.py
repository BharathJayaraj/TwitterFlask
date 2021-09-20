import os


class Config(object):
    try:
        SECRET_KEY = os.environ.get('SECRET_KEY', "!9m@S-dThyIlW[pHQbN^")
        TWITTER_OAUTH_CLIENT_KEY = os.environ.get("API_KEY", "")
        TWITTER_OAUTH_CLIENT_SECRET = os.environ.get("API_SECRET", "")
        TWITTER_OAUTH_ACCESS_KEY = os.environ.get("ACCESS_KEY", "")
        TWITTER_OAUTH_ACCESS_SECRET = os.environ.get("ACCESS_SECRET", "")
        SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI", "")
    except Exception as err:
        print("Exception occurred in configuration file.", err)
