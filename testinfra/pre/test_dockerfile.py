#!/usr/bin/env python3
"""Checks on Dockerfile.

Can be run before trying to build the container
"""

import pytest


@pytest.fixture(scope="module")
def docker_file(host):
    """Use Dockerfile as fixture for tests."""
    return host.file("Dockerfile")


def test_kostenstelle(docker_file):
    """Verify Kostenstelle in Dockerfile"""
    assert docker_file.contains(r"LABEL kostenstelle=\w")


def test_version(docker_file):
    assert docker_file.contains("httpd:2.4.53")
