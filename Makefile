.PHONY: install run debug clean lint lint-strict

install:
	...
run:
	python3 a_maze_ing.py config.txt
debug:
	python3 -m pdb a_maze_ing.py config.txt
lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
lint-strict:
	flake8 .
	mypy . --strict
clean:
	find . -type d \( -name "__pycache__" -o -name ".mypy_cache" -o -name ".pytest_cache" \) -exec rm -rf {} +
