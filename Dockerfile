FROM python:3.8-slim

# Language pack
RUN set -ex \
    && apt-get update -yqq \
    && apt-get install -y locales \
    && sed -i '/pl_PL.UTF-8 UTF-8/s/^# //g' /etc/locale.gen \
    && locale-gen \
    && export LANG=pl_PL.UTF-8 \
    && apt-get autoremove -yqq --purge \
    && apt-get clean

# Copy the most important files for setup
COPY requirements.txt setup_config.py ./

# Python application preparation
RUN set -ex; \
    pip install -r requirements.txt; \
    python setup_config.py

COPY . /

CMD gunicorn app:server -b :8080