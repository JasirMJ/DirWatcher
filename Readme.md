# DirWatcher

DirWatcher which runs a long running background time looped scheduled task with results being exposed via REST API.

##### Note : This has been verified in windows OS only

#### Contains:
* REST API Server
* Long running background task using Celery

#### Available Actions
* Long running background task which will monitor the configured directory at a scheduled interval of configured time
* Can change any configuration of Directory that needs to be monitored
* Will get some details like files created and deleted details


### How to Run

##### 1.Make sure python 3 is installed

##### 2.Clone project
* Hope everybody knows it
##### 3.Create and activate virtual environment

##### 4.Install requirements
* pip install -r requirements.txt

##### 5.Apply migrations
* python manage.py migrate

##### 6.Run Server
* python manage.py runserver

##### 7.Run redis, im running redis in windows with docker 
* docker run -p 6379:6379 -d redis:5

##### 8.Run Celery Worker 
* celery -A dirwatcher worker -l info --pool=solo

##### 9.Run Celery Beat 
* celery -A dirwatcher beat -l info 

#### API

http://localhost:8000/dir/

#### GET API : 
* http://localhost:8000/dir/path=E:\TestDir -- To get all available files in the specified path, this will create new record if the path not in the record
##### Response     
```
{
        "Status": true,
        "Message": "",
        "Data": {
            "id": 43,
            "name": "E:\\TestDir",
            "path": "E:\\TestDir",
            "created_at": "2022-05-27T13:59:41.870740Z",
            "updated_at": "2022-05-28T18:08:32.956147Z",
            "is_deleted": false,
            "files": [
                {
                    "id": 159,
                    "name": "alramool_52.66.91.176-20220506-122204-fhuwyj.wpress",
                    "created_at": "2022-05-27T13:59:41.886737Z",
                    "updated_at": "2022-05-27T13:59:41.886737Z",
                    "deleted_at": null,
                    "is_deleted": false,
                    "record": 43
                },
                {
                    "id": 160,
                    "name": "fluido_13.233.183.118-20220506-121918-ozcpfq.wpress",
                    "created_at": "2022-05-27T13:59:41.891739Z",
                    "updated_at": "2022-05-27T13:59:41.891739Z",
                    "deleted_at": null,
                    "is_deleted": false,
                    "record": 43
                }
            ],
            "monitor_enabled": true
        }
    }
```
#### POST API :
*  http://localhost:8000/dir/ //with the below payload to enable or disable monitoring
##### Payload
    'id': '43', // pass id for update record
    'name': 'E:\TestDir',
    'path': 'E:\TestDir',
    'monitor_enabled': '1' // to enable monitoring set to 1 else to 0

##### Response 
```
{
    "Status": true,
    "Message": "Data updated",
    "Data": {
        "id": 43,
        "name": "E:\\TestDir",
        "path": "E:\\TestDir",
        "created_at": "2022-05-27T13:59:41.870740Z",
        "updated_at": "2022-05-28T20:06:26.272933Z",
        "is_deleted": false,
        "files": [
            {
                "id": 159,
                "name": "alramool_52.66.91.176-20220506-122204-fhuwyj.wpress",
                "created_at": "2022-05-27T13:59:41.886737Z",
                "updated_at": "2022-05-27T13:59:41.886737Z",
                "deleted_at": null,
                "is_deleted": false,
                "record": 43
            },
            {
                "id": 160,
                "name": "fluido_13.233.183.118-20220506-121918-ozcpfq.wpress",
                "created_at": "2022-05-27T13:59:41.891739Z",
                "updated_at": "2022-05-27T13:59:41.891739Z",
                "deleted_at": null,
                "is_deleted": false,
                "record": 43
            }
        ],
        "monitor_enabled": true
    }
}
```
