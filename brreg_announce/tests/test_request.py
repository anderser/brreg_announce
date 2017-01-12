from __future__ import print_function
from unittest import TestCase
from xmltest import XMLAssertions

# import pyklima
# from pyklima.wsklima_requests import wsKlimaRequest
# from pyklima.wsklima_parser import parse_get_data, parse_get_elements_from_timeserie_type_station


# class TestWsRequest(TestCase,XMLAssertions):
#     def testversion(self):
#         s = pyklima.version()
#         self.assertEqual(s, 0.1)

#     def testgetMetData(self):
#         wr = wsKlimaRequest('getMetData', {
#             'timeserietypeID': 2,
#             'format': "",
#             'from': '2016-10-01',
#             'to': '2016-10-02',
#             'stations': [54110, 12290],
#             'elements': ['TA'],
#             'hours': range(0, 24),
#             'months': "",
#             'username': ""}
#         ).get()
#         self.assertXPathNodeCount(wr.content, 1, './/{http://no/met/metdata/MetService.wsdl}getMetDataResponse/return/timeStamp/item[0]')

#     def testgetMetDataHourly(self):
#         wr = wsKlimaRequest('getMetData', {
#             'timeserietypeID': 2,
#             'format': "",
#             'from': '2016-12-26',
#             'to': '2016-12-26',
#             'stations': [52535],
#             'elements': ['FFM', FFX],
#             'hours': range(0, 24),
#             'months': "",
#             'username': ""}
#         ).get()
#         self.assertXPathNodeCount(wr.content, 1, './/{http://no/met/metdata/MetService.wsdl}getMetDataResponse/return/timeStamp/item[0]')


#     def testgetElementsFromTimeserieTypeStation(self):

#         wr = wsKlimaRequest('getElementsFromTimeserieTypeStation', {
#             'timeserietypeID': 0,
#             'stations': [50540],
#             }
#         ).get()
#         self.assertXPathNodeCount(wr.content, 1, './/{http://no/met/metdata/MetService.wsdl}getElementsFromTimeserieTypeStationResponse/return/item[0]/elemCode[0]')

#     def testGetStationProperties(self):

#         wr = wsKlimaRequest('getStationsProperties', {
#             'stations': [54110],
#             'username': ""}
#         ).get()
#         self.assertXPathNodeCount(wr.content, 1, './/{http://no/met/metdata/MetService.wsdl}getStationsPropertiesResponse/return/item[0]/amsl[0]')


#     def testgetTimeserieTypesProperties(self):
#         wr = wsKlimaRequest('getTimeserieTypesProperties', {
#             'language': None
#             }).get()
#         self.assertXPathNodeCount(wr.content, 1, './/{http://no/met/metdata/MetService.wsdl}getTimeserieTypesPropertiesResponse/return/item[0]/elemTable[0]')
