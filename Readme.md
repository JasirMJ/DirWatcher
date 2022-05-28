
###run celery worker

celery -A dirwatcher worker -l info --loglevel=debug
celery -A dirwatcher worker -l info --pool=solo

celery -A dirwatcher beat -l info
celery -A dirwatcher beat --loglevel=debug


celery -A dirwatcher worker --beat --loglevel=debug