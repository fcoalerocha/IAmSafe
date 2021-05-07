FROM python:3.9-buster as builder

RUN mkdir /install
WORKDIR /install

#better copy a requirements file 
RUN pip install --upgrade pip
COPY requirements.txt /requirements.txt
RUN pip install --prefix=/install -r /requirements.txt

FROM python:3.9.1-slim

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

ENV MAIN game

RUN apt-get update; apt-get install -y curl

#Copy dependencies precompiled from builder image
#this is a multistage build, using this you can get slimmer images
COPY --from=builder /install /usr/local

WORKDIR /code

# Switching to a non-root user, please refer to https://aka.ms/vscode-docker-python-user-rights
RUN useradd appuser && chown -R appuser /code
USER appuser

COPY --chown=appuser:appuser . /code

#RUN mkdir /code/auth/static
# "Collect static files"
RUN export DJANGO_SETTINGS_MODULE="${MAIN}.settings.production" \
    && python manage.py collectstatic --noinput
RUN sed -i "s,newDomain,$DOMAIN," data/data.json
RUN sed -i "s,newName,$NAME," data/data.json

RUN sed -i 's/\r$//' docker-entrypoint.sh

EXPOSE 8000

ENTRYPOINT [ "/bin/bash" ]
CMD [ "docker-entrypoint.sh" ]
