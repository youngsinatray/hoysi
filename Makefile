venv:
	python3 -m venv venv
	venv/bin/pip install -r requirements.txt

format:
	venv/bin/pip install -r requirements-tests.txt
	venv/bin/black --verbose src
	venv/bin/flake8 src

format/check:
	venv/bin/pip install -r requirements-tests.txt
	venv/bin/black --verbose src
	venv/bin/flake8 src

run: venv
	PYTHONPATH=src venv/bin/python src/main.py --email=$(email) --password=$(password) --box-name=$(box-name) --box-id=$(box-id) --days-in-advance=$(days-in-advance)

tests: venv format/check
	venv/bin/pip install -r requirements-tests.txt
	PYTHONPATH=src venv/bin/pytest src/tests

docker/build:
	docker build --no-cache	--tag=fitbot .

docker/tests:
	docker run fitbot /bin/sh -c 'make tests'

docker/check:
	PYTHONPATH=src venv/bin/python src/main.py --email=$(email) --password=$(password) --box-name=$(box-name) --box-id=$(box-id) --days-in-advance=$(days-in-advance) > output.txt
	cat output.txt