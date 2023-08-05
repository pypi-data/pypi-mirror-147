#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Utility functions."""

import re
import html

# HTML parser was renamed in python 3.x
try:
    from html.parser import HTMLParser
except ImportError:
    from HTMLParser import HTMLParser

_parser = HTMLParser()


def clean_comment_body(body):
    """Returns given comment HTML as plaintext.

    Converts all HTML tags and entities within 4chan comments
    into human-readable text equivalents.
    """
    body = html.unescape(body)
    body = re.sub(r'<a [^>]+>(.+?)</a>', r'\1', body)
    body = body.replace('<br>', '\n')
    body = body.replace('<p class="body-line ltr ">', '\n')
    body = re.sub(r'<.+?>', '', body)
    return body
