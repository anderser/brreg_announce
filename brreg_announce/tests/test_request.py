from unittest import TestCase

import brreg_announce
from brreg_announce.brreg import Announcements

class TestRequest(TestCase):

    def test_get_search_response_code(self):
        ann = Announcements()
        searchresults = ann.build_search()
        self.assertEqual(searchresults.status_code, 200)

    def test_search_parse(self):
        ann = Announcements()
        searchresults = ann.search(datoFra='12.01.2019', datoTil='12.01.2019')
        print(searchresults)
        self.assertEqual(searchresults['meta']['searchdate'], '12.01.2019')
        self.assertEqual('name' in searchresults['results'][0], True)
        self.assertEqual(len(searchresults['results']), 31)

    def test_search_parse_empty_res(self):
        ann = Announcements()
        searchresults = ann.search(datoFra='22.01.2017', datoTil='22.01.2017')
        self.assertEqual(searchresults['meta']['searchdate'], '22.01.2017')
        self.assertEqual(searchresults['results'], [])
        self.assertEqual(searchresults['count'], 0)
    
    def test_search_konkurser_bergen(self):
        ann = Announcements()
        searchresults = ann.search(
            datoFra='01.09.2019', 
            datoTil='22.10.2019',
            id_niva1=51,
            id_region=300,
            id_fylke=12,
            id_kommune=1201
        )
        self.assertEqual(searchresults['count'], 128)
        
        