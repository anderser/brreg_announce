import sys
sys.path.append("../brreg_announce")
from brreg_announce.brreg import Announcements

ann = Announcements()
res = ann.search(
    fetch_details=True,
    datoFra='01.01.2019', 
    datoTil='01.11.2019',
    id_niva1=51,
    id_niva2=56,
    #id_niva3=41,
    id_region=300,
    id_fylke=12,
    id_kommune=1201
)
#res = ann.search(
#    orgnr=954478696
#)

print(res)


#endring forretningsadresse: &id_niva1=9&id_niva2=38&id_niva3=41