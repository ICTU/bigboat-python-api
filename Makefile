.PHONY: all
all: release

.PHONY: release
release: pylint clean tag build push upload

.PHONY: setup
setup:
	pip install -r requirements.txt
	pip install setuptools wheel

.PHONY: get_version
get_version: 
	$(eval VERSION=v$(shell python setup.py --version))
	python setup.py --version

.PHONY: pylint
pylint:
	pylint *.py bigboat/*.py

.PHONY: tag
tag: get_version
	git tag $(VERSION)

.PHONY: build
build:
	python setup.py sdist
	python setup.py bdist_wheel --universal

.PHONY: push
push: get_version
	git push origin $(VERSION)

.PHONY: upload
upload:
	twine upload dist/*

.PHONY: clean
clean:
	rm -rf build/ dist/ bigboat.egg-info
