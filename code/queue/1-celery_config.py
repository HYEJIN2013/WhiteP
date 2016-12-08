# Define Queues
CELERY_QUEUES = (
    Queue('default', routing_key='task.#'),
    Queue('orchestrator', routing_key='orchestrator.#'),
)

# Set default values for non-manually-routed tasks
CELERY_DEFAULT_QUEUE = 'default'
CELERY_DEFAULT_EXCHANGE = 'tasks'
CELERY_DEFAULT_EXCHANGE_TYPE = 'topic'
CELERY_DEFAULT_ROUTING_KEY = 'task.default'

# Strict routes for restricted tasks
CELERY_ROUTES = {
    'orchestrator.update': {
        'queue': 'orchestrator',
        'routing_key': 'orchestrator.update',
    },
}
