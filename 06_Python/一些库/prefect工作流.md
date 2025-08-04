# prefect工作流

## 工作流

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

### 其他flow设置项

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

### task设置项

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

## 