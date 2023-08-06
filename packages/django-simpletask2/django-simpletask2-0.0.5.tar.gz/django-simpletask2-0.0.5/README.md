# django-simpletask2

基于Django框架的一款简单的异步任务管理器。任务的业务逻辑均写在自定义任务数据模型中。通过Redis队列触发任务执行。

## 文档

- [中文文档]()
- [English Document]()

## 安装

```
pip install django-simpletask2
```

## 使用

**pro/settings.py**

```
INSTALLED_APPS = [
    ...
    'django_simpletask2',
    ...
]

# requires redis cache backend, see django-redis for detail
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://:xxx@xxx:6379/0?decode_responses=True",
    }
}

DJANGO_SIMPLETASK2_TASK_PULL_TIMEOUT = 5 # optional, default to 5
DJANGO_SIMPLETASK2_REDIS_NAME = "default" # optional, default to "default"
DJANGO_SIMPLETASK2_ACLKEY = "Bqud27SzhUymXDuBfvYNHJWQm0i4FdUB" # optional, default to settings.SECRET_KEY
```

**pro/urls.py**

```
from django.urls import path
from django.urls import include

urlpatterns = [
    ...
    path('django-simpletask2/', include("django_simpletask2.urls")),
    ....
]
```

**app/models.py**

```
import base64
from django.db import models
from django_simpletask2.models import SimpleTask


class HelloTask(SimpleTask):
    name = models.CharField(max_length=64)

    def do_task_main(self, payload):
        return "Hello, {}. Nice to meet you!".format(self.name)

class WorldTask(SimpleTask):
    url = models.CharField(max_length=128)
    content = models.TextField(null=True, blank=True)

    is_multi_steps = True
    final_step = 2

    def do_task_main_step1(self, payload=None):
        return {
            "proxy": {
                "method": "GET",
                "url": self.url,
            }
        }
    
    def do_task_main_step2(self, payload=None):
        payload = payload or {}
        base64content = payload.get("proxied_content", None)
        if base64content:
            try:
                content = base64.decodebytes(base64content.encode()).decode("utf-8")
                success = True
            except UnicodeDecodeError:
                try:
                    content = base64.decodebytes(base64content.encode()).decode("gb18030")
                    success = True
                except UnicodeDecodeError:
                    content = "failed to decode proxied_content: {0}".format(base64content)
                    success = False
        else:
            content = payload.get("proxied_error", None)
            success = False

        self.content = content
        self.save()

        if success:
            return True
        else:
            raise RuntimeError("WorldTask.do_task_main_step2 failed....")
```

**etc/django-simpletask2-server-config.yml**

```
redis: "redis://:xxx@xxx:6379/0?decode_responses=True"
channels: default
server: https://localhost:80000/django-simpletask2/
aclkey: xxxx
task-pull-engine: redis
threads: 1
idle-sleep: 5
error-sleep: 5
auto-reset-task-interval: 60
do-auto-reset-task: true
```

**Start django-simpletask2-server to trigger tasks**

```
django-simpletask2-server -c etc/django-simpletask2-server-config.yml start
```

## 接口错误码

| 错误码 | 错误消息 | 错误消息（中文）|
| --- | --- | --- |
| 2910000 | system error. | 系统错误。 |
| 2910001 | please send request parameters in PAYLOAD format. | 请以PAYLOAD形式传送接口参数。|
| 2910002 | `aclkey` field is required. | `aclkey`字段是必填字段。|
| 2910003 | aclkey is wrong and access denied. | `aclkey`错误，拒绝访问。|
| 2910004 | got an already deleted task {task_info}, you may ignore this and continue. | 任务已删除，可以忽略该错误继续执行。|
| 2910005 | bad formatted task_info: {task_info}. | `task_info`格式不合法。|
| 2910006 | Simple task model {task_class_name} not exists. | 任务数据模型不存在。|
| 2910007 | task handler is not implemented, task={app_label}.{model_name}, handler={}. | 任务处理器未实现。 |
| 2910008 | task status is not READY but {status}, you can not start it again. | 任务当前状态不是READY，不能被启动。|
| 2910009 | calling {handler_name} failed with error message: {error}. | 调用任务处理函数失败。|
| 2910010 | save task done status failed with error message: {error}. | 保存程序结束状态时发生错误。|
| 2910011 | `task_info` field is required for a multi-steps task. payload={payload}. | `task_info`字段是必须的。|
| 2910012 | got NO task in channels: {channels}. | 任务通道中没有任务。|
| 2910013 | task {task_info} locked by another worker. | 任务被其它执行器锁定。|
| 2910014 | task {app_label}.{model_name}:{task_id} failed to save status with error message: {error}. | 保存任务状态时发生异常。|
| 2910015 | task {app_label}.{model_name}:{task_id} already done, to do NOTHING. | 任务{app_label}.{model_name}:{task_id}，什么都不需要做。|

## 版本历史


### v0.0.5

- 修正actions中的do_task调用问题。
- 修正ugettext_lazy问题。
- 修正与django 4.x的兼容性问题。

### v0.0.4

- 修正任务队列过长导致超期任务重复执行的问题。


### v0.0.1

- 版本首发。
