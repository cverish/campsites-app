example_filter_combos = [
    ({"code": "FOO1"}, {"code__ct": "FOO"}, "code"),
    ({"name": "foobar"}, {"name__ct": "foo"}, "name"),
    ({"state": "CT"}, {"state": "CT"}, "state"),
    ({"country": "USA"}, {"country": "USA"}, "country"),
    ({"campsite_type": "AUTH"}, {"campsite_type": "AUTH"}, "campsite_type"),
    ({"month_open": 3}, {"month_open__lt": 4}, "month_open__lt"),
    ({"month_close": 11}, {"month_close__gt": 10}, "month_close__gt"),
    (
        {"month_open": 3, "month_close": 11},
        {"month_open__lt": 4, "month_close__gt": 10},
        "month_close_and_open",
    ),
    (
        {"elevation_ft": 2000},
        {"elevation_ft__gt": 1500},
        "elevation_ft__gt",
    ),
    (
        {"elevation_ft": 2000},
        {"elevation_ft__lt": 3500},
        "elevation_ft__lt",
    ),
    (
        {"elevation_ft": 2000},
        {"elevation_ft__gt": 1500, "elevation_ft__lt": 3500},
        "elevation_ft__gt__lt",
    ),
    ({"num_campsites": 20}, {"num_campsites__gt": 15}, "num_campsites__gt"),
    ({"num_campsites": 20}, {"num_campsites__lt": 25}, "num_campsites__lt"),
    (
        {"num_campsites": 20},
        {"num_campsites__gt": 15, "num_campsites__lt": 25},
        "num_campsites__gt__lt",
    ),
    (
        {"nearest_town_distance": 100},
        {"nearest_town_distance__lt": 150},
        "nearest_town_distance__lt",
    ),
]

example_csv_content = """lon,lat,composite,code,name,type,phone,dates_open,comments,num_campsites,elevation_ft,amenities,state,nearest_town_distance,nearest_town_bearing,nearest_town
-73.098,41.651,BLAC/Black Rock State Park  SP PH:860.283.8088 early may-late sep  SITES:100  AMEN:NH DP RS approx 2.1 mi SW of Thomaston 41.651 -73.098,BLAC,Black Rock State Park,SP,860.283.8088,early may-late sep, ,100, ,NH DP RS ,CT,2.1,SW,Thomaston
-72.342,41.484,DEVI/Devils Hopyard State Park  SP PH:860.526.2336 mid apr-late sep  SITES:20  AMEN:NH RS approx 7.0 mi E of East Haddam 41.484 -72.342,DEVI,Devils Hopyard State Park,SP,860.526.2336,mid apr-late sep, ,20, ,NH RS ,CT,7.0,E,East Haddam
-71.811,41.534,GREE/Green Falls - Pachaug State Forest  SF PH:860.376.4075   SITES:20  AMEN:NH NR  41.534 -71.811,GREE,Green Falls - Pachaug State Forest,SF,860.376.4075, , ,20, ,NH NR ,CT,,,
-72.556,41.265,HAMM/Hammonasset State Park  SP PH:203.245.1817 early jun-late sep  SITES:550  AMEN:E DP DW SH RS approx 0.1 mi E of Madison 41.265 -72.556,HAMM,Hammonasset State Park,SP,203.245.1817,early jun-late sep, ,550, ,E DP DW SH RS ,CT,0.1,E,Madison
"""

example_incorrect_csv_content = """lon,lat,composite,code,name,type,phone,dates_open,comments,num_campsites,elevation_ft,amenities,state,nearest_town_distance,nearest_town_bearing,nearest_town
-73.098,41.651,,,,,,,,,,,,,,
"""
