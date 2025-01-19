build:
	rm -rf ./dist
	tox -e build
	tox -e publish -- --repository pypi
