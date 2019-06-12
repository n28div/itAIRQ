from os import environ
from urllib.parse import urlparse

DEBUG = True

if 'STAGE' in environ:
    if environ['STAGE'] == 'prod' or environ['STAGE'] == 'production':
        DEBUG = False

# Flask configuration
flask = {
    'SECRET_KEY': 'DEBUG' if DEBUG else environ['FLASK_SECRET_KEY']
}

# Redis configuration
# parse informations from REDISCLOUD_URL env variable
if 'REDISCLOUD_URL' in environ:
    url = urlparse(environ.get('REDISCLOUD_URL'))
    redis_url = url.hostname
    redis_port = url.port
    redis_password = url.password
else:
    redis_url = 'localhost'
    redis_port = 6379
    redis_password = ''

redis = {
    'URL': redis_url,
    'PORT': redis_port,
    'PASSWORD': redis_password,
    'MEMORY':  int(environ.get('REDIS_MEMORY', 5)) # in megabytes
}

# Data configurations
data = {
    'REFRESH_INTERVAL': 60 * int(environ.get('REFRESH_INTERVAL'), 15) # in seconds (60s * 15m)
}