# Modern Flask

## 性能基准

以 `gunicorn` 为服务器，以 `--workers 1 --threads 1` 为性能基准

目的是为了在容器环境下，以 `1 CPU` 为基准进行调度

## 配置

### Flask.config

使用环境变量 `CONFIG_SOURCE` 来判断配置来源，只支持 Python 类型

* 本地文件
    * `xxxx.py`
* Kubernetes 资源
    * `kubernetes://[NAMESPACE]/configmaps/[NAME]/[KEY]`
    * `kubernetes://[NAMESPACE]/secrets/[NAME]/[KEY]`
    * `kubernetes://configmaps/[NAME]/[KEY]`
    * `kubernetes://secrets/[NAME]/[KEY]`
* HTTP 资源
    * `http://xxxxx.xxxx/xxxx.py`
    * `https://xxxxx.xxxx/xxxx.py`

默认为本地文件 `config.py`

### 可观测性

可观测性框架基于 `OpenTelemetry`，使用 `Zipkin` 或者 `Jaeger` 作为导出格式, 默认启用了对以下组件的观测

* logging
* flask
* sqlalchemy
* redis

**切换导出格式**

使用 环境变量 `OTEL_EXPORTER` 切换 `zipkin` 和 `jaeger`

**设置 Kubernetes 相关环境变量**

```jsonnet
[
  {
    name: 'OTEL_EXPORTER',
    value: 'zipkin',
  },
  {
    name: 'OTEL_EXPORTER_ZIPKIN_ENDPOINT',
    value: 'http://zipkin.observability:9411/api/v2/spans',
  },
  {
    name: 'NODE_NAME',
    valueFrom: {
      fieldRef: {
        fieldPath: 'spec.nodeName',
      },
    },
  },
  {
    name: 'POD_NAME',
    valueFrom: {
      fieldRef: {
        fieldPath: 'metadata.name',
      },
    },
  },
  {
    name: 'POD_NAMESPACE',
    valueFrom: {
      fieldRef: {
        fieldPath: 'metadata.namespace',
      },
    },
  },
  {
    name: 'SERVICE_NAME',
    value: name,
  },
  {
    name: 'CONFIG_SOURCE',
    value: 'kubernetes://secrets/' + name + '-cfg/config.py',
  },
  {
    name: 'WORKLOAD_TYPE',
    value: type,
  }
]
```

**设置其他参数**

所有 `Flask.config` 中，以 `OTEL_` 开头的配置会自动写入环境变量，用以配置 `OpenTelemetry` 的其他组件

详细参考:

* https://opentelemetry-python.readthedocs.io/en/latest/exporter/zipkin/zipkin.html
* https://opentelemetry-python.readthedocs.io/en/latest/exporter/jaeger/jaeger.html
* https://opentelemetry-python-contrib.readthedocs.io/en/latest/instrumentation/logging/logging.html

**指标**

使用标准 Prometheus 库，暴露于 `/metrics` 路径下

### 数据库

使用 `SQLAlchemy` 库

`Engine` 配置来自于 `Flask.config`, 前缀 `DATABASE_ENGINE_`, 参考配置如下:

```python
DATABASE_ENGINE_URL = "sqlite+pysqlite:///:memory:"
DATABASE_ENGINE_ECHO = True
DATABASE_ENGINE_FUTURE = True
```

详细参考 https://github.com/sqlalchemy/sqlalchemy/blob/533f5718904b620be8d63f2474229945d6f8ba5d/lib/sqlalchemy/engine/create.py#L43

`Session` 配置来自于 `Flask.config`, 前缀 `DATABASE_SESSION_`, 参考配置如下:

```python
DATABASE_SESSION_AUTOFLUSH = False
```

详细参考 https://github.com/sqlalchemy/sqlalchemy/blob/533f5718904b620be8d63f2474229945d6f8ba5d/lib/sqlalchemy/orm/session.py#L3866

### Redis

使用 `Redis` 库, 配置来自于 `Flask.config`, 前缀 `REDIS_`, 参考配置如下:

```python
REDIS_HOST = "127.0.0.1"
```

详细参考 https://github.com/redis/redis-py/blob/12c17bfc436ea6784bbc8b2d327d981520858eb7/redis/client.py#L853

### 存储

目前只支持 腾讯云 COS 和 阿里云 OSS

配置来自于 `Flask.config`，前缀 `STORAGE_`，参考配置如下

**腾讯云 COS**

```python
STORAGE_VENDOR = "cos"

STORAGE_SECRET_ID = "xxxxxxxxx"
STORAGE_SECRET_KEY = "xxxxxxxxx"
STORAGE_REGION = "ap-guangzhou"
STORAGE_ENDPOINT = "xxx.xxx.com"
```

详细参考 https://github.com/tencentyun/cos-python-sdk-v5/blob/3b6e2f1bdf28ebd7e29a211105c8f4dc6b46eddd/qcloud_cos/cos_client.py#L36

**阿里云 OSS**

```python
STORAGE_VENDOR = "oss"

STORAGE_ACCESS_KEY_ID = ""
STORAGE_ACCESS_KEY_SECRET = ""
STORAGE_ENDPOINT = ""
STORAGE_BUCKET = ""
```

详细参考 https://pypi.org/project/oss2/

### Celery

使用 `Flask.config` 配置 `CELERY_` 前缀参数

## 许可证

Guo Y.K., MIT License
