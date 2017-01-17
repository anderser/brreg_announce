# Brreg announcements
This app scrapes the announcements section (kunngjøringer) of the Norwegian business registry (Brønnøysundregistrene) and returns the data on a structured format.

# Install

`pip install git+https://github.com/anderser/brreg_announce.git`

# Usage

Search for announcements

```
from brreg_announce.brreg import Announcements
announcements = Announcements()
searchresults = announcements.search(
    datoFra='12.01.2017',
    datoTil='12.01.2017',
    id_fylke=12)
```

Returns object with keys for `meta`, `count` and `results`

#Tests

Run test using `nosetests`

Run single test with i.e `nosetests brreg_announce.test.XX`

Run tests with debug logging: `nosetests --debug=brreg_announce`