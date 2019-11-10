from unittest import TestCase

from brreg_announce.brreg import Announcements

class TestRequest(TestCase):

    def test_get_search_response_code(self):
        ann = Announcements()
        searchresults = ann.build_search()
        self.assertEqual(searchresults.status_code, 200)

    def test_search_parse(self):
        ann = Announcements()
        searchresults = ann.search(datoFra='12.01.2019', datoTil='12.01.2019')
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

    def test_single_announcement(self):
        ann = Announcements()
        obj = {'name': 'ÅSANE PARFYMERI & HUDPLEIE AS', 'orgnr': '914771056', 'detail_link': 'https://w2.brreg.no/kunngjoring/hent_en.jsp?kid=20190000699070&sokeverdi=914771056&spraak=nb', 'event': 'Konkursåpning', 'date': '30.09.2019'}
        #obj = {'name': 'VILLA EUROPA', 'orgnr': '988473618', 'detail_link': 'https://w2.brreg.no/kunngjoring/hent_en.jsp?kid=20190000713571&sokeverdi=988473618&spraak=nb', 'event': 'Konkursåpning', 'date': '11.10.2019'}
        res = ann.get_single_announcement(obj['detail_link'], obj['event'])
        self.assertEqual(res['Saksnr'], '19-142694KON-BERG/')
        
    def test_search_and_return_konkurser_bergen(self):
        ann = Announcements()
        res = ann.search(
            fetch_details=True,
            datoFra='01.09.2019', 
            datoTil='10.09.2019',
            id_niva1=51,
            #id_niva2=54,
            id_region=300,
            id_fylke=12,
            id_kommune=1201
        )
        self.assertEqual(searchresults['count'], 128)
        