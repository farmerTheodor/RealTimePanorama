import os
import time
import pytest
import urllib.request

def test_ping_server_gives_200():
    connection = urllib.request.urlopen(os.environ['APP_URL']+"/")
    assert connection.getcode() == 200

def test_stream_returns_200():
    connection = urllib.request.urlopen(os.environ['APP_URL'])
    assert connection.getcode() == 200