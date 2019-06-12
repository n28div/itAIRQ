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
    'URL': environ.get('REDIS_URL', 'localhost'),
    'PORT': int(environ.get('REDIS_PORT', 6379)),
    'DB': int(environ.get('REDIS_PORT', 0)),
    'MEMORY':  int(environ.get('REDIS_MEMORY', 5)) # in megabytes
}

# Data configurations
data = {
    'REFRESH_INTERVAL': 60 * int(environ.get('REFRESH_INTERVAL'), 15) # in seconds (60s * 15m)
}