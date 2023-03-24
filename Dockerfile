FROM python:3.11
WORKDIR /app
RUN apt-get update && \
    apt-get install -y --no-install-recommends firefox-esr
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY tests.py .
CMD pytest -v -s tests.py