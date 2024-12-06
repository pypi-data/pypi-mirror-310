#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016  <>
#
# Distributed under terms of the MIT license.

# Python modules
from __future__ import unicode_literals

# Third-party modules
import pytest

# Project modules
from fnapy.utils import Message
from fnapy.exceptions import FnapyResponseError
from tests import make_requests_get_mock, fake_manager
from tests.offline import create_context_for_requests


def test_query_messages(monkeypatch, fake_manager):
    context = create_context_for_requests(monkeypatch, fake_manager,
                                          'query_messages', 'messages_query')
    with context:
        fake_manager.query_messages(paging=1, results_count=100)


def test_query_messages_with_invalid_chars_in_xml_and_auto_escape(monkeypatch, fake_manager):
    """
    When `xml_auto_escape=True` any invalid char in the XML should be removed
    from the response
    """
    context = create_context_for_requests(
        monkeypatch,
        fake_manager,
        'query_messages_with_invalid_chars_in_xml',
        'messages_query',
    )
    with context:
        fake_manager.query_messages(paging=1, results_count=100)


def test_query_messages_with_invalid_chars_in_xml_and_no_auto_escape(monkeypatch, fake_manager):
    """
    When `xml_auto_escape=False` any invalid char in the XML should raise a
    `FnapyResponseError`
    """
    context = create_context_for_requests(
        monkeypatch,
        fake_manager,
        'query_messages_with_invalid_chars_in_xml',
        'messages_query',
    )
    fake_manager.xml_auto_escape = False
    with context:
        with pytest.raises(FnapyResponseError):
            fake_manager.query_messages(paging=1, results_count=100)


def test_update_messages(monkeypatch, fake_manager):
    context = create_context_for_requests(monkeypatch, fake_manager,
                                          'update_messages', 'messages_update')
    with context:
        message1 = Message(action='mark_as_read',
                           id=u'6F9EF013-6387-F433-C3F5-4AAEF32AA317')
        message1.subject = 'order_information'
        fake_manager.update_messages([message1])
