ACTIVATE_VENV = pipenv run

build-docker-local:
	@$(ACTIVATE_VENV) docker-compose --verbose -f deploy/local/compose.yml build main


start-docker-local:
	@$(ACTIVATE_VENV) docker-compose -f deploy/local/compose.yml up

start-instance:
	@python manage.py collectstatic --no-input
	@supervisord
