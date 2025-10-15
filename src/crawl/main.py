#!/usr/bin/env python3
import logging
from datetime import datetime, timedelta, timezone
from functools import partial
from os import environ
from time import sleep

from sirene3 import ApiClient, Configuration, UniteLegaleApi
from tqdm import trange

from crawl.cursor import ApiCursor

DATE_FMT = "%Y-%m-%d"

API_PAGESIZE = 1000  # Max page size
API_RETURNFIELDS = ",".join(
    {
        # Unité légale
        "siren",
        "dateCreationUniteLegale",
        "categorieEntreprise",
        "prenom1UniteLegale",
        "prenom2UniteLegale",
        "prenom3UniteLegale",
        "prenom4UniteLegale",
        "prenomUsuelUniteLegale",
        "pseudonymeUniteLegale",
        # Variables historisées (periodesUniteLegale)
        "denominationUniteLegale",
        "nomUsageUniteLegale",
        "denominationUniteLegale",
        "denominationUsuelle1UniteLegale",
        "denominationUsuelle2UniteLegale",
        "denominationUsuelle3UniteLegale",
        "categorieJuridiqueUniteLegale",
        "activitePrincipaleUniteLegale",
        "caractereEmployeurUniteLegale",
    }
)

API_KEY = environ["SIRENE_API_KEY"]


client_config = Configuration(api_key=dict(ApiKeyAuth=API_KEY))
###
# client_proxy = "http://127.0.0.1:8080"
# client_verify_ssl = False
###

client = ApiClient(client_config)

unite_legale = UniteLegaleApi(client)

cursor = ApiCursor()


DATE_TODAY = datetime.now(timezone.utc)
DATE_YESTERDAY = DATE_TODAY - timedelta(days=1)

API_QUERYPARAM = (
    f"dateCreationUniteLegale:[{DATE_YESTERDAY.strftime(DATE_FMT)}"
    f" TO {DATE_TODAY.strftime(DATE_FMT)}]"
    " AND periode(categorieJuridiqueUniteLegale:5*)"
)

_get_unite_legale_with_defaults = partial(
    unite_legale.find_by_post_unite_legale,
    q=API_QUERYPARAM,
    champs=API_RETURNFIELDS,
    var_date=DATE_TODAY.strftime(DATE_FMT),
    nombre=API_PAGESIZE,
    masquer_valeurs_nulles=True,
)
get_unite_legale_with_cursor = cursor.use(_get_unite_legale_with_defaults)


def iter_unites_legales():
    results = get_unite_legale_with_cursor()
    if not results:
        raise RuntimeError("Empty API response.")

    total = results.header.total or 0
    yield results

    for start_index in trange(0, total, API_PAGESIZE):
        try:
            results = get_unite_legale_with_cursor(debut=start_index)
            if results:
                yield results
        except Exception as exc:
            logging.error(exc)
        finally:
            sleep(1)


def main():
    logging.info("Job started.")

    for unite_legale in iter_unites_legales():
        ...


if __name__ == "__main__":
    main()
