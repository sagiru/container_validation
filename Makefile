#!/bin/make

ARGS=
OUTPUT?=text

ifeq ($(OUTPUT),junit)
	ARGS=--test-report cst-report.xml
endif

.PHONY: test
test: cst testinfra

.PHONY: cst
cst: clean
	container-structure-test test --image myapache:latest --config cst/config.yaml -o $(OUTPUT) $(ARGS)

.PHONY: testinfra
testinfra: testinfra-pre
	echo "Test container image"
	. .venv/bin/activate
	py.test -v testinfra/container

testinfra-pre: .venv require-pytest
	echo "Test dockerfile before build"
	. .venv/bin/activate
	py.test -v testinfra/pre

.venv:
	python3 -m venv .venv
	. .venv/bin/activate
	pip install -r requirements.txt

.PHONY: require-pytest
require-pytest:
	if [[ -z  $$(which py.test) ]]; then
		echo "Trying to install py.test (package python3-pytest)"
		sudo apt install python3-pytest
	fi

.PHONY: build
build:
	docker build . -t myapache:latest

.PHONY: clean
clean:
	rm -f cst-report.xml

.ONESHELL:

SHELL := /bin/bash
SHELLFLAGS: -ceu

ifndef DEBUG
.SILENT:
endif
