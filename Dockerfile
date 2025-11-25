FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt
COPY . /app
CMD ["bash"]
