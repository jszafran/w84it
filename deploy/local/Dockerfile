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

WORKDIR /app

COPY config/nginx/nginx.conf /etc/nginx/nginx.conf
COPY config/nginx/w84it.conf /etc/nginx/sites-enabled/api.conf
COPY config/supervisord/supervisord.conf /etc/supervisor/supervisord.conf
COPY config/supervisord/nginx.ini /etc/supervisor/supervisord.d/nginx.ini
COPY config/supervisord/w84it.ini /etc/supervisor/supervisord.d/w84it.ini

# Set the right value for the accepted header for the load balancer
RUN sed -i 's/ENV/'$env_var'/g' /etc/nginx/sites-enabled/w84it.conf

COPY ./manage.py /app
COPY ./Makefile /app
COPY ./Pipfile /app
COPY ./Pipfile.lock /app

RUN pipenv install --system

COPY ./w84i_project /app
COPY ./users /app
COPY ./public /app
COPY ./products /app
COPY ./pages /app
COPY ./commons /app

# Entrypoint for docker
ENTRYPOINT ["make"]
CMD ["start-instance"]
