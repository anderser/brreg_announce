from __future__ import print_function
from unittest import TestCase
from xmltest import XMLAssertions

import brreg_announce
from brreg_announce.brreg import Announcements

class TestRequest(TestCase,XMLAssertions):

    def test_get_search_response_code(self):
    	ann = Announcements()
    	searchresults = ann.build_search()
    	self.assertEqual(searchresults.status_code, 200)

    def test_search_parse(self):
    	ann = Announcements()
    	searchresults = ann.search(datoFra='12.01.2017', datoTil='12.01.2017')
    	self.assertEqual(searchresults['meta']['searchdate'], '12.01.2017')
        self.assertEqual('name' in searchresults['results'][0], True)
        self.assertEqual(len(searchresults['results']), 186)

    def test_search_parse_empty_res(self):
        ann = Announcements()
        searchresults = ann.search(datoFra='22.01.2017', datoTil='22.01.2017')
        self.assertEqual(searchresults['meta']['searchdate'], '22.01.2017')
        self.assertEqual(searchresults['results'], [])
        self.assertEqual(searchresults['count'], 0)