PYTHON=python3

.PHONY: clean

all: clean install_depends run_server

install_depends:
	pip install --upgrade pip 
	pip install -r requirements.txt

run_server:
	$(PYTHON) manage.py makemigrations
	$(PYTHON) manage.py migrate
	$(PYTHON) manage.py shell < create_users.py
	$(PYTHON) manage.py runserver

clean:
	rm -rf backend/__pycache__
	rm -rf backend/migrations/__pycache__
	rm -rf retail_analitycs/__pycache__
	rm -rf controller/__pycache__
	rm -rf model/__pycache__
	rm -rf logger/__pycache__
	
linter:
	flake8 *.py backend/*.py backend/migrations/*.py controller/*.py model/*.py retail_analitycs/*.py
	pylint --indent-string='    ' *.py backend/*.py backend/migrations/*.py controller/*.py model/*.py retail_analitycs/*.py
