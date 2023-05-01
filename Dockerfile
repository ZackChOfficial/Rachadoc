FROM python:3.10.11-slim-bullseye
ARG TAG=0.1
LABEL maintainer="zack.ch.official@gmail.com"

RUN apt-get update \
  && apt-get upgrade -qq --no-install-recommends \
  && apt-get install -qq --no-install-recommends \
  &&  apt-get install binutils libproj-dev gdal-bin -y \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Install pyenv
ENV PYENV_ROOT /home/python/.pyenv
ENV PATH $PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH
RUN curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash

# Upgrade pip and install pipenv
RUN pip install -U pip pipenv

ENV PROJECT_DIR=/projects
ENV RACHADOC_ROOT=$PROJECT_DIR/rachadoc \
  PYTHONPATH=$PROJECT_DIR/rachadoc \
  PYTHONUNBUFFERED=1 \
  DEBUG=False \
  LOGLEVEL=INFO \
  DJANGO_SETTINGS_MODULE=rachadoc.core.settings

# Prepare in-container folder structure
RUN mkdir -p $PROJECT_DIR 

WORKDIR $PROJECT_DIR 

COPY . $RACHADOC_ROOT

WORKDIR $RACHADOC_ROOT

RUN pipenv --bare sync



