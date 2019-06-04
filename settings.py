from os import environ

DEBUG = True

if 'STAGE' in environ:
    if environ['STAGE'] == 'prod' or environ['STAGE'] == 'production':
        DEBUG = False

# Flask configuration
flask = {
    'SECRET_KEY': 'DEBUG' if DEBUG else environ['FLASK_SECRET_KEY']
}