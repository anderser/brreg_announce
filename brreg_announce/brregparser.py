#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import datetime as dt
#import numpy as np
from lxml import etree
from io import StringIO, BytesIO

"""
__author__: Anders G. Eriksen

"""


def parse_annoncements():
    """
    :param xml_data: string or file containing XML data
    :return: station_dict
    """
