#!/usr/bin/env python3
import pytest
import subprocess
import testinfra


@pytest.fixture(scope="session")
def host(request):
    # build local ./Dockerfile
    subprocess.check_call(["docker", "build", "-t", "myimage", "."])
    # run a container
    docker_id = (
        subprocess.check_output(["docker", "run", "-d", "myimage"]).decode().strip()
    )
    # return a testinfra connection to the container
    yield testinfra.get_host("docker://" + docker_id)
    # at the end of the test suite, destroy the container
    subprocess.check_call(["docker", "rm", "-f", docker_id])


@pytest.mark.parametrize(
    "file_path,permissions,test_pattern",
    [
        ("/etc/apache2/httpd.conf", 0o777, r"^Listen 8080$"),
        ("/usr/local/apache2/logs", 0o755, None),
    ],
)
def test_files(host, file_path, permissions, test_pattern):
    """Test files for existence and content."""
    test_file = host.file(file_path)
    assert test_file.exists
    assert test_file.mode == permissions
    if test_pattern:
        assert test_file.contains(test_pattern)


def test_user(host):
    """Test for user www-data"""
    test_user = host.user("www-data")
    assert test_user.exists


def test_service(host):
    """Test expected service (will NOT work)"""
    assert host.socket("tcp:0.0.0.0:80").is_listening
