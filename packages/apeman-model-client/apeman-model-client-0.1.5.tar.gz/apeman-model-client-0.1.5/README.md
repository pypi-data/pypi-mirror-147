#### This library enables you to report the status of tasks in your model at runtime
#### publish:
```shell
python setup.py sdist bdist_wheel
twine upload --repository-url https://test.pypi.org/legacy/ dist/*

```
#### install: `pip install apeman-model-client==0.1.0`


#### How to use
```shell
export apeman_meta_server_addr='localhost:9090'
```
```python
import os

from apeman_model_client import apemanModelClient
from apeman_model_client.model_instance_task_status import TaskStatus

client = apemanModelClient.ApemanModelServiceClient()
# report status of the model instance task
client.report(task_id='xxxx', status=TaskStatus.RUNNING, progress=0.1, message='test', token='')
# get endpoint of the model instance
client.get_endpoint(model_instance_id='test')

```
