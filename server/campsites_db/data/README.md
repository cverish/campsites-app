# Data
## Table of Contents  
[Overview](#overview)  
[Data Structure](#data-structure) 
[Explanation of Data](#explanation-of-data)
    [`composite`](#composite)
    [`campsite_type`](#campsite_type)
    [`amenities`](#amenities)

## Overview

Data for this project was pulled from [USCampgrounds.info](http://www.uscampgrounds.info/) - Tom Hillegass deserves all of the credit for his tireless work in compiling over 13,000 public campgrounds in the US and Canada. The data was last updated in 2014.

## Data Structure
The data contained in this folder comes directly from [the website](http://www.uscampgrounds.info/takeit.html) (with column headers added).

Processing of the data can be found in `campsites_api/utils/process_data.py`. Here, I've fixed up datatypes, processed the `dates_open` column into two separate `month_open` and `month_closed` integer values representing the number of the month, `date_open` and `date_closed`, and separated out the amenities. These processing functions are split out into `utils.py` for readability. A list of `Campsite`s is returned by this script.

## Explanation of Data

I've pulled some explanations of the data from the website for clarity.

### `composite`
The `composite` field contains all of the data fields compacted into one field for a single-field GPS or mapping software display. This composite field is unprocessed from the original source.

### `campsite_type`
Indicates the type of campsite. All campsites are public.

| Type   | Description                      |
| ------ | -------------------------------- |
| `AMC`  | Appalachian Mountain Club        |
| `AUTH` | Authority                        |
| `BLM`  | US Bureau of Land Management     |
| `BOR`  | US Bureau of Reclamation         |
| `CNP`  | Canadian National Park           |
| `COE`  | US Corps of Engineers            |
| `CP`   | County/City/Regional Park        |
| `MIL`  | Military Only                    |
| `NF`   | US National Forest               |
| `NM`   | National Monument                |
| `NP`   | US National Park                 |
| `NRA`  | National Recreation Area         |
| `NS`   | National Seashore                |
| `NWR`  | National Wildlife Refuge         |
| `PP`   | Canadian Provincial Park         |
| `PR`   | Canadian Provinical Reserve      |
| `RES`  | Native American Reservation      |
| `SB`   | State Beach                      |
| `SCA`  | State Conservation Area          |
| `SF`   | State Forest                     |
| `SFW`  | State Fish and Wildlife          |
| `SP`   | State Park                       |
| `SPR`  | State Preserve                   |
| `SR`   | State Reservation                |
| `SRA`  | State Rec. Area                  |
| `SRVA` | State Recreational Vehicle Area  |
| `TVA`  | Tennessee Valley Authority       |
| `USFW` | US Fish and Wildlife             | 
| `UTIL` | Utility                          |
| `null` | Unknown Type                     |

## Amenities:
A string of amenity codes. A lack of a code does not indicate that the campground does not have that service, but that data is not available.

| Code      | Description                           |
| --------- | ------------------------------------- |
| `NH`      | no RV hookups                         |
| `E`       | electric hookup                       | 
| `WE`      | electric and water hookup             |
| `WES`     | electric, water, and sewage hookup    |
| `DP`      | sanitary dump                         |
| `ND`      | no dump                               |
| `{num}ft` | max RV length in feet                 |
| `FT`      | flush toilet                          |
| `VT`      | vault toilet                          |
| `FTVT`    | some flush toilets, some vault        |
| `PT`      | pit toilet                            |
| `NT`      | no toilets                            |
| `DW`      | drinking water at campground          |
| `NW`      | no drinking water                     |
| `SH`      | showers                               |
| `NS`      | no showers                            |
| `RS`      | accepts reservations                  |
| `NR`      | no reservations                       |
| `PA`      | pets allowed                          |
| `NP`      | no pets allowed                       |
| `L$`      | free or under $12                     |
