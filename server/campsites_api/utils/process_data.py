import codecs
import csv
from typing import List

from fastapi import HTTPException, UploadFile

import campsites_api.utils.process_data_utils as ut
from campsites_api.dto import CampsiteDTO


def process_data(file: UploadFile) -> List[CampsiteDTO]:
    """
    Takes in a csv file containing campsite data, returns a list of processed
    CampsiteDTO objects.

    Parameters:
        file (UploadFile): file uploaded via API

    Returns:
        processed_campsites (List[CampsiteDTO]): phone number as string
            of numbers only (or None)
    """
    raw_rows = []

    reader = csv.DictReader(codecs.iterdecode(file.file, "utf-8"))
    for row in reader:
        raw_rows.append(row)

    if len(raw_rows) == 0:
        raise HTTPException(status_code=422, detail="Empty file uploaded.")

    # using a typed list so it auto-converts values and gives helpful
    # failures for unclean data
    processed_campsites: List[CampsiteDTO] = []

    # process each row
    for row in raw_rows:
        # go through all values and strip spaces.
        # also change values to null if empty string
        row = {k: v.strip() if v.strip() != "" else None for (k, v) in row.items()}

        # a few entries have "dispersed" for number of campsites; as this is not
        # a known number, setting value to null
        row["num_campsites"] = (
            row["num_campsites"]
            if row["num_campsites"] is not None and row["num_campsites"].isdigit()
            else None
        )

        # casting campsite type correctly
        row["campsite_type"] = row["type"]

        # phone number
        row["phone"] = ut.process_phone_number(row["phone"])

        # dates
        dates = ut.process_dates(row["dates_open"])
        row = row | dates

        # country
        row["country"] = ut.process_country(row["state"])

        # amenities
        amenities = ut.process_amenities(row["amenities"])
        row = row | amenities
        try:
            processed_campsites.append(CampsiteDTO(**row))
        except Exception:
            raise HTTPException(status_code=422, detail="CSV file in incorrect format.")

    file.file.close()
    return processed_campsites
