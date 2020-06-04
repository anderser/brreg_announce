# Brreg announcements
This app scrapes the announcements section (kunngjøringer) of the Norwegian business registry (Brønnøysundregistrene) and returns the data on a structured format.

## Install

`pip install git+https://github.com/anderser/brreg_announce.git`

## Usage

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

## Tests

Run test using `pipenv run python -m unittest`

Run single test: `pipenv run python -m unittest brreg_announce.tests.test_request.TestRequest.test_search_konkurser_openings_vestland`

## Info on data source

More info on data source: https://w2.brreg.no/kunngjoring/
Info on licensing/usage of data: https://www.brreg.no/produkter-og-tjenester/betingelser/