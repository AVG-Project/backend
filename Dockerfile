FROM python:3.10.15

#RUN useradd -rms /bin/bash Istok && chmod 777 /opt /run
WORKDIR /Istok
#RUN mkdir /Istok/staticfiles && mkdir /Istok/media && chown -R Istok:Istok /Istok && chmod 755 /Istok
#COPY --chown=Istok:Istok . .
COPY . .

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y curl && apt-get clean
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

#USER Istok

CMD python manage.py makemigrations \
    && python manage.py migrate \
    && python manage.py collectstatic --noinput \
    && gunicorn Istok.wsgi:application -b 0.0.0.0:8000

