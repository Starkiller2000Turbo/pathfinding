WORKDIR = algorythms

style:
	isort .
	black .
	flake8 .
	mypy .

run_wave:
	python wave_main.py

run_astar:
	python astar_main.py

req:
	pip install -r requirements.txt

style_req:
	pip install -r style-requirements.txt
