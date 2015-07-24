test:
	tox

unit:
	py.test -v --cov-report term-missing --cov libtree tests

acceptance:
	behave tests/features

style:
	flake8 --show-source libtree
	flake8 --show-source --ignore=F811,F821 tests

style-verbose:
	flake8 -v --show-source libtree
	flake8 -v --show-source --ignore=F811,F821 tests

clean:
	find . -name '*.pyc' -exec rm -f {} \;
	find libtree -name "__pycache__" | xargs rm -rf
	find tests -name "__pycache__" | xargs rm -rf
	rm -f coverage.xml
	rm -rf *.egg-info
	rm -rf .tox/
	rm -rf build/
	rm -rf dist/
	rm -rf junit/
