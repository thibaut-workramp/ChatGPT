FROM python:3.10-slim

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

RUN mkdir -p /usr/src/app
RUN mkdir -p /usr/src/app/templates
RUN mkdir -p /usr/src/app/static
WORKDIR /usr/src/app

COPY templates/index.html templates/index.html
COPY static/background.jpg static/background.jpg
COPY static/stylesheet.css static/stylesheet.css

COPY api_keys_provider.py api_keys_provider.py
COPY utils.py utils.py
COPY base_task_solver_bot.py base_task_solver_bot.py
COPY json_filter_bot.py json_filter_bot.py
COPY server.py server.py

ENTRYPOINT ["python", "server.py"]
