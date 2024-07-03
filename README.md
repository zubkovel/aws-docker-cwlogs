# aws-docker-cwlogs

aws-docker-cwlogs is a Python script that broadcasts the log of a running docker container.

## Preparation
#### Activate the Virtual Environment

```
python3 -m venv venv && source venv/bin/activate
```
#### Install Python Libaries

```
python -m pip install -r requirement.txt
```


## Usage

```python main.py --docker-image python --bash-command $'pip install pip -U && pip
install tqdm && python -c \"import time\ncounter = 0\nwhile
True:\n\tprint(counter)\n\tcounter = counter + 1\n\ttime.sleep(0.1)\"'
--aws-cloudwatch-group test-task-group-1 --aws-cloudwatch-stream test-task-stream-1
--aws-access-key-id ... --aws-secret-access-key ... --aws-region ...
```
