#!/usr/bin/env python3
import pytest
from .context import *

FIRST_KEY='install'

@pytest.fixture
def y():
    y = ymm.load_file(TEST_FILE)
    y.env.set('debug', True)
    return y

def yexec(y, s):
    args = Args([s])
    result = ymm.exec(y,args)
    return result

def test_exec(y):
    result = yexec(y, 'install')
    assert FIRST_KEY in result[0]

def test_shell(y):
    s = "$ ls"
    result = y.execute(s, "shell")
    assert "test" in result
    result = yexec(y, 'echo')
    assert '"A":"B"' in result[0]

def test_call(y):
    result = yexec(y, 'call')
    assert '"A":"B"' in result[0]

def test_eval(y):
    result = yexec(y, 'python')
    assert 4 in result#[0]
    result = yexec(y, 'pvar')
    assert 4 in result#[0]

def test_pipe(y):
    result = yexec(y, 'pipe')
    assert "Hello" in result[0]
    assert "Hello" in result[1]

def test_match(y):
    result = yexec(y, 'path')
    assert 'B' in result[1]
