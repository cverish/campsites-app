import re
from typing import Union


def process_phone_number(phone_number_str: Union[str, None]) -> Union[str, None]:
    """
    Removes all special characters from the phone number

    Parameters:
        phone_number_str (str | None): raw phone number string (or None, if does not exist)

    Returns:
        phone_number (str | None): phone number as string of numbers only (or None)
    """
    if phone_number_str is None:
        return None
    return re.sub("[^A-Za-z0-9]+", "", phone_number_str)


def process_dates(date_open_str: Union[str, None]) -> dict:
    """
    Takes in a string indicating when the camp opens and closes (e.g. "mid may-late sep").
    Processes this string into month_open and month_close, represented by an integer
    value indicating the month

    Parameters:
        date_open_str (str | None): date string for camp opening

    Returns:
        dates_dict (dict): contains "month_open" and "month_close" as integers
    """
    dates_dict = {
        "month_open": None,
        "month_close": None,
    }
    if date_open_str is None:
        return dates_dict

    if date_open_str == "all year":
        dates_dict["month_open"] = 1
        dates_dict["month_close"] = 12
        return dates_dict

    dates_map = {
        "jan": 1,
        "feb": 2,
        "mar": 3,
        "apr": 4,
        "may": 5,
        "jun": 6,
        "jul": 7,
        "aug": 8,
        "sep": 9,
        "oct": 10,
        "nov": 11,
        "dec": 12,
    }

    # replace "-" with spaces to ensure we get a clean split
    date_open_arr = date_open_str.replace("-", " ").split(" ")
    # find first string in array that contains a month
    open_str = date_open_arr.pop(0)
    while open_str not in dates_map.keys() and len(date_open_arr) > 0:
        open_str = date_open_arr.pop(0)
    for month in dates_map.keys():
        if month == open_str:
            dates_dict["month_open"] = dates_map[month]

    if len(date_open_arr) == 0:
        return dates_dict

    # date open has been found; repeat process to find closing month
    close_str = date_open_arr.pop(0)
    while close_str not in dates_map.keys() and len(date_open_arr) > 0:
        close_str = date_open_arr.pop(0)
    for month in dates_map.keys():
        if month in close_str:
            dates_dict["month_close"] = dates_map[month]

    return dates_dict


def process_country(state_str: str) -> str:
    """
    takes in a string representation of a state or province and returns
    the country. Only compares against the list of Canadian provinces
    because it is either Canada OR United States

    Parameters:
        state_str (str | None): 2-character string representing state or province

    Returns:
        country (str): country ("United States" or "Canada")
    """
    canadian_provinces = [
        "AB",
        "BC",
        "MB",
        "NB",
        "NL",
        "NT",
        "NS",
        "NU",
        "ON",
        "PE",
        "QC",
        "SK",
        "YT",
    ]
    return "CAN" if state_str in canadian_provinces else "USA"


def process_amenities(amenity_str: Union[str, None]) -> dict:
    """
    processes the raw string of amenity codes into a dictionary.
    amenity codes can be found under the map at
    http://www.uscampgrounds.info/

    The amenity list may not be complete, so None values indicate
    that information is not available.

    Parameters:
        amenity_str (str | None): space-separated string of amenity codes

    Returns:
        amenity_dict (dict): a dictionary of processed amenity values
    """

    amenity_dict = {
        "has_water_hookup": None,
        "has_electric_hookup": None,
        "has_sewer_hookup": None,
        "has_sanitary_dump": None,
        "max_rv_length": None,
        "has_toilets": None,
        "toilet_type": None,
        "has_drinking_water": None,
        "has_showers": None,
        "accepts_reservations": None,
        "accepts_pets": None,
        "low_no_fee": None,
    }

    # if amenities is None, skip over processing and return amenity_dict as-is
    if amenity_str is None:
        return amenity_dict

    amenities = amenity_str.strip().split(" ")

    for amenity_code in amenities:
        # hookups
        if amenity_code in ["NH", "E", "WE", "WES"]:
            amenity_dict["has_electric_hookup"] = True if "E" in amenity_code else False
            amenity_dict["has_water_hookup"] = True if "W" in amenity_code else False
            amenity_dict["has_sewer_hookup"] = True if "S" in amenity_code else False
            if amenity_code != "NH":
                amenity_dict["has_rv_hookup"] = True
            elif amenity_code == "NH":
                amenity_dict["has_rv_hookup"] = False

        # sanitary dump
        if amenity_code in ["DP", "NP"]:
            amenity_dict["has_sanitary_dump"] = True if amenity_code == "DP" else False

        # max RV length
        if "ft" in amenity_code:
            length = int(amenity_code.split("ft")[0])
            amenity_dict["max_rv_length"] = length

        # toilets
        if amenity_code in ["FT", "VT", "FTVT", "PT", "NT"]:
            if amenity_code == "NT":
                amenity_dict["has_toilets"] = False
            else:
                amenity_dict["has_toilets"] = True
                toilet_map = {
                    "FT": "flush",
                    "VT": "vault",
                    "FTVT": "mixed",
                    "PT": "pit",
                }
                amenity_dict["toilet_type"] = toilet_map[amenity_code]

        # drinking water
        if amenity_code in ["DW", "NW"]:
            amenity_dict["has_drinking_water"] = True if amenity_code == "DW" else False

        # showers
        if amenity_code in ["SH", "NS"]:
            amenity_dict["has_showers"] = True if amenity_code == "SH" else False

        # reservations
        if amenity_code in ["RS", "NR"]:
            amenity_dict["accepts_reservations"] = (
                True if amenity_code == "RS" else False
            )

        # pets
        if amenity_code in ["PA", "NP"]:
            amenity_dict["accepts_pets"] = True if amenity_code == "PA" else False

        # low fee
        if amenity_code == "L$":
            amenity_dict["low_no_fee"] = True

    return amenity_dict
