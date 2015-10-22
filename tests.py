#! /usr/bin/env python3

import nose
from message import Message

def test_simple():
    assert True

def test_default_levels():
    logger = Message()
    assert logger.get_file_level() == 'info'
    assert logger.get_print_level() == 'debug'
