#DirWatcher

DirWatcher which runs a long running background time looped scheduled task with results being exposed via REST API.

#####Note : This has been verified in windows OS only

####Contains:
* REST API Server
* Long running background task using Celery

####Available Actions
* Long running background task which will monitor the configured directory at a scheduled interval of configured time
* Can change any configuration of Directory that needs to be monitored
* Will get some details like files created and deleted details


###How to Run

#####1.Make sure python 3 is installed

#####2.Clone project
* Hope every one do this

#####3.Create and activate virtual environment

#####4.Install requirements
* pip install -r requirements.txt

#####5.Apply migrations
* python manage.py migrate

#####6.Run Server
* python manage.py runserver

#####7.Run redis, im running redis in windows with docker 
* docker run -p 6379:6379 -d redis:5

#####8.Run Celery Worker 
* celery -A dirwatcher worker -l info --pool=solo

#####9.Run Celery Beat 
* celery -A dirwatcher beat -l info 

