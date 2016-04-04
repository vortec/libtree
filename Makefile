.PHONY: test unit acceptance style style-verbose docs clean

test:
	tox

unit:
	py.test -v --cov-report term-missing --cov libtree tests

acceptance:
	behave tests/features

style:
	flake8 --show-source --ignore=E731 libtree
	flake8 --show-source --ignore=E731,F811,F821 tests

style-verbose:
	flake8 -v --show-source --ignore=E731 libtree
	flake8 -v --show-source --ignore=E731,F811,F821 tests

docs:
	make -C docs html

clean:
	find . -name '*.pyc' -exec rm -f {} \;
	find libtree -name "__pycache__" | xargs rm -rf
	find tests -name "__pycache__" | xargs rm -rf
	make -C docs clean
	rm -f coverage.xml
	rm -rf *.egg-info
	rm -rf .cache/
	rm -rf .eggs/
	rm -rf .tox/
	rm -rf build/
	rm -rf docs/build/
	rm -rf dist/
	rm -rf junit/
