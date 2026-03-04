PYTHON = python3
CONFIG = config.txt
MAIN = a_maze_ing.py

install:
	pip install -r requirements.txt

run:
	$(PYTHON) $(MAIN) $(CONFIG)

debug:
	$(PYTHON) -m pdb $(MAIN) $(CONFIG)

clean:
	rm -rf __pycache__
	rm -rf output
	rm -rf .mypy_cache

lint:
	flake8