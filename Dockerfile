FROM mcr.microsoft.com/playwright/python:v1.65.2-noble
WORKDIR /usr/local/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m playwright install --with-deps

COPY comics ./comics
COPY cogs ./cogs
COPY oona.py ./oona.py
CMD ["python", "oona.py"]
