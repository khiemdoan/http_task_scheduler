Build

```
docker build . --tag http_task_scheduler
```

Run

```
docker run -it --rm \
--name http_task_scheduler \
--volume "$PWD/src":/src \
--publish 6000:6000 \
http_task_scheduler:latest
```