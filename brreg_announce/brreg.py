#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import urllib
import requests
from datetime import datetime, timedelta
import time
import logging
from lxml import html
from io import StringIO, BytesIO
import json
"""
Author: Anders G. Eriksen
"""

logger = logging.getLogger(__name__)


class Announcements():

    def __init__(self):
        self.BASE_URL = 'https://w2.brreg.no/kunngjoring/'
        self.SEARCH_BASE_URL = '%s%s' % (self.BASE_URL, 'kombisok.jsp')
        self.SEARCH_BASE_URL_COMPANY = '%s%s' % (self.BASE_URL, 'hent_nr.jsp')

    def build_search(self, **kwargs):
        """
        Search announcements
        https://w2.brreg.no/kunngjoring/kombisok.jsp?datoFra=09.01.2017
        &datoTil=&id_region=300&id_fylke=12&&id_kommune=-+-+-&id_niva1=1&id_bransje1=0
        """

        yesterday = datetime.now() - timedelta(days=1)

        orgnr = kwargs.get('orgnr', None)
        
        #if searching for one company, drop all other params
        if orgnr:
            self.search_params = {
                'orgnr': orgnr,
                'deleted': 'true'
            }
            search_url = self.SEARCH_BASE_URL_COMPANY
        else:
            self.search_params = {
                'datoFra': kwargs.get('datoFra', yesterday.strftime('%d.%m.%Y')),
                'datoTil': kwargs.get('datoTil', None),
                'id_region': kwargs.get('id_region', 300),
                'id_fylke': kwargs.get('id_fylke', 12),
                'id_kommune': kwargs.get('id_kommune', None),
                'id_niva1': kwargs.get('id_niva1', 1),
                'id_niva2': kwargs.get('id_niva2', ''),
                'id_niva3': kwargs.get('id_niva3', ''),
                'id_bransje1': kwargs.get('id_bransje1', 0),
            }
            search_url = self.SEARCH_BASE_URL
        logger.debug("Sending search request")
        r = requests.get(search_url, params=self.search_params)

        return r

    def _parse_resultstable(self, table, metainfo):

        data = list()
        rows = table.xpath('//tr')
        for row in rows:
            cols = row.xpath('td')
            if len(cols) > 4:
                element = dict()
                element['name'] = cols[1].text_content().strip()
                # check if this is a real row or one of the one-word
                # header rows
                if element['name'] != '':
                    element['orgnr'] = cols[3].text_content(
                    ).strip().replace(' ', '')
                    
                    #if searching for events on niva3, then table looks different
                    if self.search_params['id_niva3'] != '':
                        element['detail_link'] = '%s%s' % (
                            self.BASE_URL, cols[1].xpath('.//a/@href')[0])
                        # event type is not given in table rows, so get from meta
                        element['event'] = metainfo['event']


                
                    # when only one date is given, then table looks different
                    elif self.search_params['datoFra'] == self.search_params['datoTil']:
                        element['detail_link'] = '%s%s' % (
                            self.BASE_URL, cols[5].xpath('.//a/@href')[0])
                        element['event'] = cols[5].text_content().strip()
                        element['date'] = self.search_params['datoFra']
                    else:
                        element['detail_link'] = '%s%s' % (
                            self.BASE_URL, cols[7].xpath('.//a/@href')[0])
                        element['event'] = cols[7].text_content().strip()
                        element['date'] = cols[5].text_content().strip()

                    data.append(element)

        return data

    def _parse_metatable(self, table):

        keyvalues = table.xpath('.//tr/td//strong/text()')
        metainfo = dict(zip(['searchdate', 'place', 'event'], keyvalues[1::2]))
        return metainfo

    def parse_search(self, result):

        logger.debug("Parsing")
        tree = html.fromstring(result.content)
        # logger.debug(result.text)

        tables = tree.xpath('//div[@id="pagecontent"]/table')

        metainfo = self._parse_metatable(tables[1])
        logger.debug('Meta: %s' % metainfo)

        try:
            count = int(tables[2].xpath('.//td//strong/text()')[1].strip())
        except IndexError:
            logger.debug('No announcements found')
            results = []
            count = 0
        else:
            logger.debug('Count: %s' % count)
            results = self._parse_resultstable(tables[3], metainfo)
            resulttable = tables[3]

        # logger.debug(results)
        response = {
            'meta': metainfo,
            'count': count,
            'results': results
        }
        return response

    def search(self, fetch_details=False, **kwargs):

        results = self.build_search(**kwargs)
        parsed = self.parse_search(results)

        if fetch_details is True:
            res_with_details = []
            for obj in parsed['results']:
                # only if company
                if len(obj['orgnr']) > 6:
                    logger.debug(obj['detail_link'])
                    details = self.get_single_announcement(
                        obj['detail_link'], obj['event'])
                    obj.update(details)
                logger.debug(json.dumps(obj, ensure_ascii=False, indent=4))
                res_with_details.append(obj)
                time.sleep(1)
            parsed['results'] = res_with_details

        return parsed

    def text(self, elt):

        # Are there multiple text elements in the element?

        text_elements = elt.xpath('./text()')
        if len(text_elements) > 1:
            stripped_elements = [t.strip() for t in text_elements]
            # remove empty strings from list
            return list(filter(None, stripped_elements))
        else:
            return elt.text_content().replace(u'\xa0', u' ').strip()

    def _parse_key_value_from_table(self, table):

        tabledata = {}
        for tr in table.xpath('.//tr'):
            tds = tr.xpath('./td')
            # extract the keys from the first td, remove colon
            key = tds[0].text_content().strip().replace(':', '')
            # extract text elements from the rest of the tds in this row
            for td in tds[1:len(tds)]:
                tabledata[key] = self.text(td)

        return tabledata

    def _parse_single_page(self, html_content, event_type):
        tree = html.fromstring(html_content)
        maintable = tree.xpath('//div[@id="pagecontent"]/table')[1]

        content = {}
        content_tables = maintable.xpath('.//table')
        for table in content_tables:
            tabledata = self._parse_key_value_from_table(table)
            content.update(tabledata)
        try:
            if event_type == 'Konkursåpning':
                content['bostyrer'] = maintable.xpath('.//tr[6]/td/text()')[1:4]

            if event_type == 'Avslutning av bobehandling':
                content['dividende'] = maintable.xpath(
                    './tr/td/span[5]/text()')[0].strip()
                content['utlodningsdag'] = maintable.xpath(
                    './tr/td/text()')[13]

        except IndexError as e:
            content['error'] = str(e)
        return content

    def get_single_announcement(self, uri, event_type):

        r = requests.get(uri)
        details = self._parse_single_page(r.content, event_type)
        return details
