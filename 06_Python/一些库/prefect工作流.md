# prefect工作流

## 创建工作流

### 1.普通工作流

```python
from prefect import flow

@flow
def test_flow():
    print("Hello world")

if __name__ == "__main__":
    test_flow()
```

### 2.类工作流

```python
from prefect import flow

class FlowClass:
    # 实例方法
    @flow
    def instance_methods_flow(self):
        print("实例方法流水线")
    
    # 类方法
    @flow
    @classmethod
    def class_methods_flow(cls):
        print("类方法流水线")

    # 静态方法
    @flow
    @staticmethod
    def static_methods_flow():
        print("静态方法流水线")

if __name__ == "__main__":  
    FlowClass().instance_methods_flow()
    FlowClass.class_methods_flow()
    FlowClass.static_methods_flow()
```

### 3.flow嵌套

```python
from prefect import flow, task
import random

@task
def generate_a_number():
    return random.randint(0, 100)

@flow(name="even number")
def is_even_number(number: int):
    return (number % 2) == 0

@flow(name="even or odd")
def even_or_odd():
    number = generate_a_number()
    if is_even_number(number):
        print(f"the number {number} is even")
    else:
        print(f"the number {number} is odd")

even_or_odd()

```

### 其他flow设置项（部分）

|arge|description|
|----|----|
|decription|工作流描述|
|name|工作流名，不配置则是函数名|
|retries|工作流失败的重试次数|
|retry_delay_seconds|重试间隔，仅在`retries!=0`时生效|
|flow_run_name|flow运行实例的名称|
|task_runner|控制任务流执行方式|
|timeout_second|工作流运行的最长时间，超时工作流失败|
|validate_parameters|bool值，表示是否用Pydantic验证传递给流程的参数，默认为`True`|
|version|版本控制|

### task设置项（部分）

|arge|description|
|----|----|
|name|任务名，不配置则是函数名|
|decription|任务描述|
|tags|任务标签，提升工作流的可管理性和可观测性|
|timeout_second|任务运行的最长时间，超时任务失败|
|cache_key_fn|自定义缓存方式|
|cache_policy|缓存策略，确定生成缓存时使用那些信息：`INPUTS`, `TASK_SOURCE`, `RUN_ID`, `FLOW_PARAMETERS`, `NO_CACHE`, 可以使用`+`组合|
|cache_expiration|缓存数据时效，默认永不过去|
|retries|工作流失败的重试次数|
|retry_delay_seconds|重试间隔，仅在`retries!=0`时生效|
|log_prints|是否打印日志|

## `assets`: 跟踪数据输出

### 1.基本使用

```python
from prefect import flow
from prefect.assets import materialize

@materialize("s3://my-bucket/processed-data.csv")
def process_data(data:dict) -> dict:
    # 这里进数据处理
    return

@flow(name="数据处理", flow_run_name="数据处理运行中")
def data_pipeline(data: dict):
    process_data(data)

data_pipeline({'flowName': '数据处理'})
```

### 2.资产依赖关系

prefect会自动从任务流中推断资产依赖关系

### 3.动态资产物化

使用`with_options`更改资产key或依赖

## 重试机制

### `retries`\\`retry_delay_seconds`

```python
from prefect import flow, task
from prefect.tasks import exponential_backoff
import time

@task(retries=2, retry_delay_seconds=5)
def retry_task_1():
    raise Exception("restry task")

@task(retries=2, retry_delay_seconds=[2, 4])
def retry_task_2():
    raise Exception("restry task")

@task(retries=2, retry_delay_seconds=exponential_backoff(backoff_factor=2))
def retry_task_3():
    raise Exception("restry task")

@flow(retries=2, retry_delay_seconds=1, version="1.0.0")
def retry_flow(type:int):
    if type == 1:
        retry_task_1()
    elif type == 2:
        retry_task_2()
    elif type == 3:
        retry_task_3()

try:
    retry_flow(3)
except:
    pass
```

> [!NOTE]
> 重试次数是在首次执行后重试的次数

### 自定义重试条件`retry_condition_fn`

```python
import httpx
from prefect import flow, task

def retry_handler(task, task_run, state) -> bool:
    try:
        state.result()
    except:
        return True
    
@task(retries=1, retry_condition_fn=retry_handler)
def api_call_task(url):
    response = httpx.get(url)
    response.raise_for_status()
    return response.json()

@flow(name="重试条件")
def retry_condition_flow():
    api_call_task("https://docs.prefect.io")

try:
    retry_condition_flow()
except:
    pass
```

### 随机重试时间添加随机`retry_jitter_factor`

设置随机抖动（**测试效果不佳**）

## 任务并发

### `.submit`

**`.submit`默认情况下，任务通过`ThreadPoolTaskRunner`提交，在线程池中并发**

```python
from prefect import flow, task
from prefect.futures import wait

@task(name="测试并发")
def conccurrent_task(i: int):
    print(f"第{i}个任务1")
    print(f"第{i}个任务2")
          
@flow(name="并发测试任务流", log_prints=True)
def conccurrent_flow():
    tmp = []
    for i in range(10):
        tmp.append(conccurrent_task.submit(i))

    wait(tmp)

conccurrent_flow()
```

### `.map`\\`unmapped()`

**`.map`默认情况下，任务通过`ThreadPoolTaskRunner`提交，在线程池中并发**

```python
from prefect import flow, task, unmapped
from prefect.futures import wait
from prefect_dask.task_runners import DaskTaskRunner
import time

@task(name="map_unmap")
def map_task(a, b):
    return a + sum(b)
          
@flow(name="map任务流")
def map_flow(val1, val2):
    vars = range(5)
    tmp = map_task.map(val1, unmapped(val2))

    return tmp.result()

if __name__ == "__main__":
    res = map_flow([4, 5, 6], [1, 2, 3])
    try:
        print(res)
        assert res == [10, 11, 12]
    except:
        print("fuck")
```

