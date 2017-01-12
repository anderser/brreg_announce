from __future__ import print_function
from unittest import TestCase
from xmltest import XMLAssertions
import json
# import pyklima
# from pyklima.wsklima_requests import wsKlimaRequest
# from pyklima.wsklima_parser import parse_get_data, parse_get_elements_from_timeserie_type_station,parse_get_stations_properties

# def date_handler(obj):
#     if hasattr(obj, 'isoformat'):
#         return obj.isoformat()
#     else:
#         raise TypeError

# class TestWsParser(TestCase,XMLAssertions):

#     def testparseGetMetData(self):
#     	wr = wsKlimaRequest('getMetData', {
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
#     	parsed = parse_get_data(wr.content)
#     	self.assertEqual(parsed[0]['value'], 6.3)
#         self.assertEqual(parsed[0]['station'], '54110')


#     def testparseGetStationProperties(self):

#         wr = wsKlimaRequest('getStationsProperties', {
#             'stations': [54110, 12290],
#             'username': ""}
#         ).get()
#         #print(wr.content)
#         parsed = parse_get_stations_properties(wr.content)
#         #self.assertEqual(parsed[0]['value'], 6.3)
#         #self.assertEqual(parsed[0]['station'], '54110')

#     def testparseElementsFromTimeserieTypeStation(self):

#         wr = wsKlimaRequest('getElementsFromTimeserieTypeStation', {
#             'timeserietypeID': 0,
#             'stations': [50540],
#             }
#         ).get()
#         parsed = parse_get_elements_from_timeserie_type_station(wr.content)
#         print(json.dumps(parsed, default=date_handler))