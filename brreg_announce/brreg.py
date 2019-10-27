#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import urllib
import requests
from datetime import datetime, timedelta
import logging
from lxml import html
from io import StringIO, BytesIO
"""
Author: Anders G. Eriksen
"""

logger = logging.getLogger(__name__)

class Announcements():

	def __init__(self):
		self.BASE_URL = 'https://w2.brreg.no/kunngjoring/'
		self.SEARCH_BASE_URL = '%s%s' % (self.BASE_URL, 'kombisok.jsp')

	def build_search(self, **kwargs):
		"""
		Search announcements
		https://w2.brreg.no/kunngjoring/kombisok.jsp?datoFra=09.01.2017
		&datoTil=&id_region=300&id_fylke=12&&id_kommune=-+-+-&id_niva1=1&id_bransje1=0
		"""

		yesterday = datetime.now() - timedelta(days=1)

		self.search_params = {
			'datoFra': kwargs.get('datoFra',yesterday.strftime('%d.%m.%Y')),
			'datoTil': kwargs.get('datoTil',None),
			'id_region': kwargs.get('id_region',300),
			'id_fylke': kwargs.get('id_fylke',12),
			'id_kommune': kwargs.get('id_kommune',None),
			'id_niva1': kwargs.get('id_niva1',1),
			'id_bransje1': kwargs.get('id_bransje1',0),
		}
		logger.debug("Sending search request")
		r = requests.get(self.SEARCH_BASE_URL, params=self.search_params)

		return r

	def _parse_resultstable(self, table):

		data = list()
		rows = table.xpath('//tr')
		for row in rows:
			cols = row.xpath('td')
			if len(cols) > 4:
				element = dict()
				element['name'] = cols[1].text_content().strip()
				#check if this is a real row or one of the one-word/empty header rows
				if element['name'] != '':
					element['orgnr'] = cols[3].text_content().strip().replace(' ','')
					
					#when only one date is given, then table looks different
					if self.search_params['datoFra'] == self.search_params['datoTil']:
						element['detail_link'] = '%s%s' % (self.BASE_URL, cols[5].xpath('.//a/@href')[0])
						element['event'] = cols[5].text_content().strip()
						element['date'] = self.search_params['datoFra']
					else:
						element['detail_link'] = '%s%s' % (self.BASE_URL, cols[7].xpath('.//a/@href')[0])
						element['event'] = cols[7].text_content().strip()
						element['date'] = cols[5].text_content().strip()

					data.append(element)

		return data

	def _parse_metatable(self, table):

		keyvalues = table.xpath('.//tr/td//strong/text()')
		metainfo = dict(zip(['searchdate', 'place','event'], keyvalues[1::2]))
		return metainfo

	def parse_search(self, result):

		logger.debug("Parsing")
		tree = html.fromstring(result.content)
		#logger.debug(result.text)

		tables = tree.xpath('//div[@id="pagecontent"]/table')

		metainfo = self._parse_metatable(tables[1])
		logger.debug('Meta: %s' % metainfo )

		try:
			count = int(tables[2].xpath('.//td//strong/text()')[1].strip())
		except IndexError:
			logger.debug('No announcements found')
			results = []
			count = 0
		else:
			logger.debug('Count: %s' % count )
			results = self._parse_resultstable(tables[3])
			resulttable = tables[3]

		logger.debug(results)
		response = {
			'meta': metainfo,
			'count': count,
			'results': results
		}
		return response


	def search(self, **kwargs):

		results = self.build_search(**kwargs)
		parsed = self.parse_search(results)
		return parsed

	def _parse_single_page(self, html_content):
		tree = html.fromstring(html_content)
		table = tree.xpath('//div[@id="pagecontent"]/table')[1]

		content = {}
		content['tingrett'] = table.xpath('.//tr[6]/td/span[2]/text()')
		content['konkurs_aapnet_dato'] = table.xpath('.//tr[6]/td[1]/table[3]/tbody[1]/tr[1]/td[2]/text()')[0].strip()
		content['konkurs_aapnet_etter'] = table.xpath('.//tr[6]/td[1]/table[4]/tbody[1]/tr[1]/td[2]/span/text()')[0].strip()
		content['saksnummer'] = table.xpath('.//tr[6]/td[1]/table[5]/tbody[1]/tr[1]/td[2]/text()')[0].strip()
		content['bostyrer'] = table.xpath('.//tr[6]/td/text()')[1:4]
		logger.debug(content)
		return table

	def get_single_announcement(self, uri, event_type):

		r = requests.get(uri)
		return self._parse_single_page(r.content)
