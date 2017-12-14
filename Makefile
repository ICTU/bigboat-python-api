COVERAGE=coverage
TEST=-m unittest discover -s tests -p '*.py'

.PHONY: all
all: release

.PHONY: release
release: pylint test clean tag build push upload

.PHONY: setup
setup:
	pip install -r requirements.txt
	pip install setuptools wheel

.PHONY: get_version
get_version: get_setup_version get_init_version
	if [ "${SETUP_VERSION}" != "${INIT_VERSION}" ]; then \
		echo "Version mismatch"; \
		exit 1; \
	fi
	$(eval VERSION=$(SETUP_VERSION))

.PHONY: get_init_version
get_init_version:
	$(eval INIT_VERSION=v$(shell grep __version__ bigboat/__init__.py | sed -E "s/__version__ = .([0-9.]+)./\\1/"))
	$(info Version in __init__.py: $(INIT_VERSION))
	if [ -z "${INIT_VERSION}" ]; then \
		echo "Could not parse version"; \
		exit 1; \
	fi

.PHONY: get_setup_version
get_setup_version:
	$(eval SETUP_VERSION=v$(shell python setup.py --version))
	$(info Version in setup.py: $(SETUP_VERSION))

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

.PHONY: test
test:
	python $(TEST)

.PHONY: coverage
coverage:
	$(COVERAGE) run $(TEST)
	$(COVERAGE) report -m

.PHONY: clean
clean:
	rm -rf build/ dist/ bigboat.egg-info .coverage
