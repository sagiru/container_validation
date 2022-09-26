#!/bin/make

ARGS=
OUTPUT?=text

ifeq ($(OUTPUT),junit)
	ARGS=--test-report cst-report.xml
endif

.PHONY: test
test: cst

.PHONY: cst
cst: clean
	container-structure-test test --image myapache:latest --config cst/config.yaml -o $(OUTPUT) $(ARGS)

.PHONY: build
build:
	docker build . -t myapache:latest

.PHONY: clean
clean:
	rm -f cst-report.xml

.ONESHELL:
ifndef DEBUG
.SILENT:
endif
