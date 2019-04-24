FROM python:3.7.3-alpine3.9

RUN apk update
RUN apk add libffi-dev make g++ linux-headers postgresql-dev nginx nano git bash
RUN mkdir /app

# Add www-data user and make it owner of /var/lib/nginx or it will cause permission errors
RUN adduser -u 82 -D -S -G www-data www-data
RUN chown -R www-data:www-data /var/lib/nginx

# Build folders for logs and supervisor
RUN mkdir /etc/supervisor
RUN mkdir /etc/supervisor/supervisord.d
RUN mkdir /var/log/uwsgi
RUN mkdir /var/log/supervisor
RUN mkdir /var/run/supervisor
RUN mkdir /var/run/uwsgi
RUN pip install pipenv==2018.11.26
RUN pip install supervisor==4.0.2
RUN mkdir /var/run/nginx

WORKDIR /app

COPY ./Pipfile /app
COPY ./Pipfile.lock /app
# Install needed deps
RUN pipenv install --dev --system


COPY config/nginx/nginx.conf /etc/nginx/nginx.conf
COPY config/nginx/w84it.conf /etc/nginx/sites-enabled/api.conf
COPY config/supervisord.conf /etc/supervisor/supervisord.conf
COPY config/nginx.ini /etc/supervisor/supervisord.d/nginx.ini
COPY config/w84it.ini /etc/supervisor/supervisord.d/w84it.ini
COPY config/uwsgi.ini /app

COPY ./manage.py /app
COPY ./Makefile /app


COPY ./w84i_project /app/w84i_project
COPY ./users /app/users
COPY ./public /app/public
COPY ./products /app/products
COPY ./pages /app/pages
COPY ./commons /app/commons
