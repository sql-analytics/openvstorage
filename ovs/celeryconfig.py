CELERY_RESULT_BACKEND = "cache"
CELERY_CACHE_BACKEND = 'memcached://127.0.0.1:11211/'
#CELERY_RESULT_BACKEND = 'amqp'
BROKER_URL = 'amqp://guest:guest@127.0.0.1:5672//'
