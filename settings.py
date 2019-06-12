from os import environ

DEBUG = True

if 'STAGE' in environ:
    if environ['STAGE'] == 'prod' or environ['STAGE'] == 'production':
        DEBUG = False

# Flask configuration
flask = {
    'SECRET_KEY': 'DEBUG' if DEBUG else environ['FLASK_SECRET_KEY']
}

# Redis configuration
redis = {
    'URL': 'localhost' if DEBUG else environ['REDIS_URL'],
    'PORT': 6379 if DEBUG else int(environ['REDIS_PORT']),
    'DB': 0 if DEBUG else int(environ['REDIS_PORT']),
    'MEMORY': 5 if DEBUG else int(environ['REDIS_MEMORY']) # in megabytes
}

# Data configurations
data = {
    'REFRESH_INTERVAL': 60 * 15 # in seconds (60s * 15m)
}