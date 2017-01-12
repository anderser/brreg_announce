#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import requests
from datetime import datetime, timedelta
import logging
from lxml import etree
from io import StringIO, BytesIO
"""
Author: Anders G. Eriksen
"""

logger = logging.getLogger(__name__)

class Announcements():

	def __init__(self):
		self.SEARCH_BASE_URL = 'https://w2.brreg.no/kunngjoring/kombisok.jsp'

	def build_search(self, **kwargs):
		"""
		Search announcements
		https://w2.brreg.no/kunngjoring/kombisok.jsp?datoFra=09.01.2017
		&datoTil=&id_region=300&id_fylke=12&&id_kommune=-+-+-&id_niva1=1&id_bransje1=0
		"""

		yesterday = datetime.now() - timedelta(days=1)

		params = {
			'datoFra': kwargs.get('datoFra',yesterday.strftime('%d.%m.%y')),
			'datoTil': kwargs.get('datoTil',None),
			'id_region': kwargs.get('id_region',300),
			'id_fylke': kwargs.get('id_fylke',12),
			'id_kommune': kwargs.get('id_fylke',None),
			'id_niva1': kwargs.get('id_niva1',1),
			'id_bransje1': kwargs.get('id_bransje1',0),
		}
		logger.debug("Sending search request")
		r = requests.get(self.SEARCH_BASE_URL)
		#logger.debug(r.text)

		return r

	def parse_search(self, result):

		logger.debug("Parsing")
		return result.text


	def search(self, **kwargs):

		results = self.build_search(**kwargs)
		parsed = self.parse_search(results)
		return parsed
