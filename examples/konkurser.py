import sys
import json
import os
sys.path.append("../brreg_announce")
from brreg_announce.brreg import Announcements

ann = Announcements()
res = ann.search(
    fetch_details=True,
    datoFra='01.01.2015', 
    datoTil='31.12.2015',
    id_niva1=51,
    id_niva2=56,
    #id_niva3=41,
    id_region=300,
    id_fylke=46,
    id_kommune=4601
)
#res = ann.search(
#    orgnr=954478696
#)
print('Rows %i' % res['count']) 

with open(os.getenv('HOME') + '/konkurser_bergen_med_detaljer_2015.json', 'w') as outfile:
    json.dump(res, outfile, ensure_ascii=False)


#endring forretningsadresse: &id_niva1=9&id_niva2=38&id_niva3=41